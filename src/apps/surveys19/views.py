import json
import logging
import csv
import operator
from functools import reduce
from itertools import islice
from collections import namedtuple

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.db.models import Count

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, StreamingHttpResponse
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter

from config.viewsets import StandardViewSet

from apps.users.models import User
from apps.surveys19.models import (
    Survey,
    Phone,
    AddressMatch,
    CityTownCode,
    FarmLocation,
    LandStatus,
    LandType,
    LandArea,
    Business,
    FarmRelatedBusiness,
    ManagementType,
    CropMarketing,
    LivestockMarketing,
    ProductType,
    Product,
    Unit,
    Loss,
    Contract,
    AnnualIncome,
    MarketType,
    IncomeRange,
    AgeScope,
    PopulationAge,
    Population,
    Relationship,
    Gender,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    LongTermHire,
    ShortTermHire,
    NoSalaryHire,
    NumberWorkers,
    Lack,
    LongTermLack,
    ShortTermLack,
    WorkType,
    Subsidy,
    Refuse,
    RefuseReason,
    Month,
    BuilderFile,
)

from .serializers import (
    ContentTypeSerializer,
    SurveySerializer,
    PhoneSerializer,
    AddressMatchSerializer,
    CityTownCodeSerializer,
    FarmLocationSerializer,
    LandStatusSerializer,
    LandTypeSerializer,
    LandAreaSerializer,
    BusinessSerializer,
    FarmRelatedBusinessSerializer,
    ManagementTypeSerializer,
    CropMarketingSerializer,
    LivestockMarketingSerializer,
    ProductTypeSerializer,
    ProductSerializer,
    UnitSerializer,
    LossSerializer,
    ContractSerializer,
    AnnualIncomeSerializer,
    MarketTypeSerializer,
    IncomeRangeSerializer,
    AgeScopeSerializer,
    PopulationAgeSerializer,
    PopulationSerializer,
    RelationshipSerializer,
    GenderSerializer,
    EducationLevelSerializer,
    FarmerWorkDaySerializer,
    LifeStyleSerializer,
    LongTermHireSerializer,
    ShortTermHireSerializer,
    NoSalaryHireSerializer,
    NumberWorkersSerializer,
    LackSerializer,
    LongTermLackSerializer,
    ShortTermLackSerializer,
    WorkTypeSerializer,
    SubsidySerializer,
    RefuseSerializer,
    RefuseReasonSerializer,
    MonthSerializer,
    BuilderFileSerializer,
    SurveySimpleSerializer,
)

logger = logging.getLogger(__file__)


class SurveyRelationGeneratorFactory:
    """ Generator Factory of Survey Relations. """

    ExportRelation = namedtuple("ExportRelation", ("generator", "column_count"))

    def __init__(self, readonly=False, filters={}, excludes={}):
        """ Make the necessary query, initial the relations in constrains and ordering by farmer_id """
        self.readonly = readonly
        self.filters = filters
        self.excludes = excludes

        self.surveys = self.get_queryset(Survey.objects.all(), filter_by_farmer_ids=False).filter(page=1).all()
        self.farmer_ids = self.surveys.values_list('farmer_id', flat=True).distinct()

        self.lookup_tables = [
            "land_areas",
            "businesses",
            "management_types",
            "lacks",
            "crop_marketings",
            "livestock_marketings",
            "annual_incomes",
            "populations",
            "long_term_hires",
            "short_term_hires",
            "no_salary_hires",
            "no_salary_hires",
            "long_term_lacks",
            "short_term_lacks",
        ]
        self.relation_count_mapping = self.get_relations_count_mapping()
        self.age_scopes = AgeScope.objects.filter(group=1).order_by("id").all()

        self.land_areas = self.ExportRelation(
            self.relation_generate(LandArea, ["type__name", "status__name", "value"]), 3
        )
        self.businesses = self.ExportRelation(
            self.relation_generate(Business, ["farm_related_business__name", "extra"]),
            2,
        )
        self.management_types = self.ExportRelation(
            self.relation_generate(ManagementType, ["name"], many_to_many=True), 1
        )
        self.crop_marketings = self.ExportRelation(
            self.relation_generate(
                CropMarketing,
                [
                    "product__code",
                    "product__name",
                    "land_number",
                    "land_area",
                    "plant_times",
                    "unit__name",
                    "year_sales",
                    "has_facility",
                    "loss__name",
                ],
            ),
            9,
        )
        self.livestock_marketings = self.ExportRelation(
            self.relation_generate(
                LivestockMarketing,
                [
                    "product__code",
                    "product__name",
                    "unit__name",
                    "raising_number",
                    "year_sales",
                    "contract__name",
                    "loss__name",
                ],
            ),
            7,
        )
        self.annual_incomes = self.ExportRelation(
            self.relation_generate(
                AnnualIncome, ["market_type__name", "income_range__name"]
            ),
            2,
        )
        self.populations = self.ExportRelation(
            self.relation_generate(
                Population,
                [
                    "relationship__name",
                    "gender__name",
                    "birth_year",
                    "education_level__name",
                    "farmer_work_day",
                    "life_style__name",
                ],
            ),
            6,
        )
        self.no_salary_hires = self.ExportRelation(
            self.relation_generate(NoSalaryHire, ["month__value", "count"]), 2
        )
        self.lacks = self.ExportRelation(
            self.relation_generate(Lack, ["name"], many_to_many=True), 1
        )
        self.long_term_hires = self.ExportRelation(
            self.long_term_hires_generate(), 3 + len(self.age_scopes)
        )
        self.short_term_hires = self.ExportRelation(
            self.short_term_hires_generate(), 3 + len(self.age_scopes)
        )
        self.long_term_lacks = self.ExportRelation(self.long_term_lacks_generate(), 4)
        self.short_term_lacks = self.ExportRelation(self.short_term_lacks_generate(), 6)

    def check_exhausted(self):
        return all([len(list(getattr(self, relation).generator)) == 0 for relation in self.lookup_tables])

    def check_relation(self, relation):
        mapping_sum = sum([self.relation_count_mapping[farmer_id][relation] for farmer_id in self.farmer_ids])
        relation_count = len(list(getattr(self, relation).generator))
        if mapping_sum != relation_count:
            print(f'Relation {relation} not fit: Mapping Sum={mapping_sum}; Relation Count={relation_count}')
            return False
        return True

    def get_queryset(self, qs, prefix='', filter_by_farmer_ids=True):
        """ Apply common filter and ordering for relation querysets """
        _default_filters = {
            f'{prefix}readonly': self.readonly,
        }
        if filter_by_farmer_ids:
            # Single survey is split into multiple Survey objects and share same farmer_id
            # The relation tables still need to filter by farmer_id
            # In case the filter/exclude below not working properly
            _default_filters[f'{prefix}farmer_id__in'] = self.farmer_ids
        _filters = {f'{prefix}{key}': value for key, value in self.filters.items()}
        _excludes = {f'{prefix}{key}': value for key, value in self.excludes.items()}
        _default_order_by = f'{prefix}farmer_id'
        return (
            qs.filter(reduce(operator.and_, [Q(**_default_filters), Q(**_filters), ~Q(**_excludes)]))
            .order_by(_default_order_by)
        )

    def relation_generate(self, model, values_list, many_to_many=False):
        """ Get the iterator of relation object values """
        prefix = "surveys__" if many_to_many else "survey__"
        qs = self.get_queryset(model.objects.all(), prefix=prefix)
        return (
            qs
            .values_list(*values_list)
            .iterator()
        )

    def get_sliced_relation_generator(self, farmer_id, relate_name):
        """ Consume the generator on at a time, base on the relation count mapping """
        mapping_info = self.relation_count_mapping[farmer_id]
        relation_count = mapping_info[relate_name]
        max_relation_count = max(mapping_info.values())
        relation = getattr(self, relate_name)
        yield from islice(relation.generator, 0, relation_count)
        for _ in range(max_relation_count - relation_count):
            yield [""] * relation.column_count

    def long_term_hires_generate(self):
        qs = self.get_queryset(LongTermHire.objects.all(), prefix='survey__')
        for lth in qs.iterator():
            values = [
                lth.work_type.name,
                lth.avg_work_day,
                ",".join(map(str, lth.months.values_list("value", flat=True))),
            ]
            for age_scope in self.age_scopes:
                search = lth.number_workers.filter(age_scope=age_scope).first()
                values.append(search.count if search else 0)
            yield tuple(values)

    def short_term_hires_generate(self):
        qs = self.get_queryset(ShortTermHire.objects.all(), prefix='survey__')
        for sth in qs.iterator():
            values = [
                ",".join(map(str, sth.work_types.values_list("name", flat=True))),
                sth.avg_work_day,
                sth.month.value,
            ]
            for age_scope in self.age_scopes:
                search = sth.number_workers.filter(age_scope=age_scope).first()
                values.append(search.count if search else 0)
            yield tuple(values)

    def long_term_lacks_generate(self):
        qs = self.get_queryset(LongTermLack.objects.all(), prefix='survey__')
        for ltl in qs.iterator():
            yield (
                ltl.work_type.name,
                ltl.count,
                ltl.avg_lack_day,
                ",".join(map(str, ltl.months.values_list("value", flat=True))),
            )

    def short_term_lacks_generate(self):
        qs = self.get_queryset(ShortTermLack.objects.all(), prefix='survey__')
        for obj in qs.iterator():
            yield (
                obj.work_type.name,
                obj.product.code,
                obj.name,
                obj.count,
                obj.avg_lack_day,
                ",".join(map(str, obj.months.values_list("value", flat=True))),
            )

    def get_relations_count_mapping(self):
        """ Lazy pre-calculate relation counts for each farmer id """
        result = {}
        qs = self.get_queryset(Survey.objects.all())

        def count_relation(relate_name):
            relations_count = (
                qs
                .values("farmer_id")
                .annotate(count=Count(relate_name))
                .values_list("farmer_id", "count")
                .order_by("farmer_id")
                .iterator()
            )
            return relations_count

        generator_lists = [count_relation(table) for table in self.lookup_tables]

        while True:
            try:
                single_result = [
                    next(generator)
                    for generator in generator_lists
                ]
                farmer_id = single_result[1][0]
                result[farmer_id] = {self.lookup_tables[i]: item[1] for i, item in enumerate(single_result)}
            except StopIteration:
                break

        return result


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class Surveys2019Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "surveys19/index.html"

    def get_context_data(self, **kwargs):
        context = super(Surveys2019Index, self).get_context_data(**kwargs)
        # template render objects
        context["farm_related_businesses"] = FarmRelatedBusiness.objects.all()
        context["management_types"] = ManagementType.objects.all()
        context["land_types"] = LandType.objects.all()
        context["income_ranges"] = IncomeRange.objects.all().order_by("minimum")
        context["market_types"] = MarketType.objects.all()
        context["genders"] = Gender.objects.all()
        context["population_age_scopes"] = AgeScope.objects.filter(group=2)
        context["hire_age_scopes"] = AgeScope.objects.filter(group=1)
        context["lacks"] = Lack.objects.all()

        # ui elements render objects
        context["contracts"] = Contract.objects.all()
        context["crop_products"] = Product.objects.filter(type=1)
        context["crop_losses"] = Loss.objects.filter(type=1)
        context["crop_units"] = Unit.objects.filter(type=1)
        context["livestock_products"] = Product.objects.filter(type=2)
        context["livestock_losses"] = Loss.objects.filter(type=2)
        context["livestock_units"] = Unit.objects.filter(type=2)
        context["education_levels"] = EducationLevel.objects.all()
        context["farmer_work_days"] = FarmerWorkDay.objects.all()
        context["genders"] = Gender.objects.all()
        context["months"] = Month.objects.all()
        context["relationships"] = Relationship.objects.all()
        context["life_styles"] = LifeStyle.objects.all()
        context["work_types"] = WorkType.objects.all()
        context["refuse_reasons"] = RefuseReason.objects.all()
        context["citytowncodes"] = CityTownCode.objects.all()

        # ui elements
        ui = {
            "cropmarketing": render_to_string(
                "surveys19/row-ui/crop-marketing.html", context
            ),
            "livestockmarketing": render_to_string(
                "surveys19/row-ui/livestock-marketing.html", context
            ),
            "population": render_to_string("surveys19/row-ui/population.html", context),
            "longtermhire": render_to_string(
                "surveys19/row-ui/long-term-hire.html", context
            ),
            "longtermlack": render_to_string(
                "surveys19/row-ui/long-term-lack.html", context
            ),
            "shorttermhire": render_to_string(
                "surveys19/row-ui/short-term-hire.html", context
            ),
            "shorttermlack": render_to_string(
                "surveys19/row-ui/short-term-lack.html", context
            ),
            "nosalaryhire": render_to_string(
                "surveys19/row-ui/no-salary-hire.html", context
            ),
        }
        context["ui"] = json.dumps(ui)
        context["fid"] = json.dumps(
            list(
                Survey.objects.filter(page=1)
                .values_list("farmer_id", flat=True)
                .distinct()
            )
        )

        return context


class BuilderFileViewSet(StandardViewSet):
    queryset = BuilderFile.objects.all()
    serializer_class = BuilderFileSerializer

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                datafile = self.request.data.get("datafile")
                token = self.request.data.get("token")
                user = self.request.user
                if not isinstance(user, User):
                    user = None

                serializer.save(user=user, datafile=datafile, token=token)
        except Exception as e:
            raise ValidationError(e)


class ContentTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            Q(app_label="surveys19", model="longtermhire")
            | Q(app_label="surveys19", model="shorttermhire")
        )


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["farmer_id"]

    def get_queryset(self, *args, **kwargs):
        fid = self.request.GET.get("fid")
        readonly = json.loads(self.request.GET.get("readonly", "false"))
        queryset = self.queryset
        if fid:
            queryset = self.queryset.filter(
                Q(farmer_id=fid) & Q(readonly=readonly)
            ).distinct()
        return queryset

    def get_object(self, pk):
        return Survey.objects.get(id=pk)

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=["GET"], detail=False, serializer_class=SurveySimpleSerializer)
    def simple_list(self, request):
        return super().list(request)

    @action(methods=["PATCH"], detail=False)
    def patch(self, request):
        try:
            data = json.loads(request.data.get("data"))
            pk = data.get("id")
            survey = self.get_object(pk)
            serializer = SurveySerializer(
                survey, data=data, partial=True
            )  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data)
            else:
                raise ValidationError(serializer.errors)

        except Exception as e:
            logger.exception(
                "Survey Patch Error: %s",
                request.path,
                extra={"status_code": 400, "request": request},
            )
            return JsonResponse(data=e.message_dict, safe=False)

    @action(methods=["GET"], detail=False, permission_classes=[IsAdminUser])
    def export(self, request):
        """A view that streams a large CSV file."""
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet
        # applications.

        def output_formatter(value):
            if isinstance(value, bool):
                value = "是" if value else "否"
            if value is None:
                value = ""
            return str(value)

        headers = [
            "農戶編號",
            "受訪人姓名",
            "電話1",
            "電話2",
            "地址與名冊相不相同",
            "地址",
            "可耕地或畜牧用地所在地區",
            "有無二代青農",
            "耕作地類型",
            "耕作地狀態",
            "耕作地面積",
            "兼營農業相關事業",
            "其他填寫",
            "主要經營型態",
            "作物代碼",
            "作物名稱",
            "耕作地編號",
            "種植面積",
            "種植次數",
            "計量單位",
            "全年產量",
            "是否使用農業設施",
            "作物備註",
            "畜禽代碼",
            "畜禽名稱",
            "計量單位",
            "年底在養數量",
            "全年銷售數量",
            "契約飼養",
            "畜禽備註",
            "銷售類型",
            "銷售額區間",
            "與戶長關係",
            "性別",
            "出生年",
            "教育程度別",
            "自家農牧業工作日數",
            "全年主要生活型態",
            "常僱主要工作類型",
            "常僱平均工作日數",
            "常僱月份",
            "常僱(44歲以下)",
            "常僱(45-64歲)",
            "常僱(65歲以上)",
            "臨僱主要工作類型",
            "臨僱平均工作日數",
            "臨僱月份",
            "臨僱(44歲以下)",
            "臨僱(45-64歲)",
            "臨僱(65歲以上)",
            "不支薪僱用月份",
            "不支薪人數",
            "短缺情形",
            "常缺工作類型",
            "常缺各月人數",
            "常缺各月平均日數",
            "常缺月份",
            "臨缺工作類型",
            "臨缺產品代碼",
            "臨缺產品名稱",
            "臨缺各月人數",
            "臨缺各月平均日數",
            "臨缺月份",
            "有無申請缺工2.0",
            "申請人數",
            "申請總時間(日)",
            "無申請缺工2.0原因",
            "調查員",
            "複審員",
        ]

        def row_generator():
            factory = SurveyRelationGeneratorFactory(excludes={'note__icontains': '無效戶'})
            errors = []
            yield headers
            for survey in factory.surveys:
                values1 = [
                    survey.farmer_id,
                    survey.farmer_name,
                    survey.phones.first().phone,
                    survey.phones.last().phone,
                    survey.address_match.match,
                    survey.address_match.address,
                    survey.farm_location.city + survey.farm_location.town,
                    survey.second,
                ]
                values2 = [
                    survey.subsidy.has_subsidy,
                    survey.subsidy.count,
                    survey.subsidy.day_delta,
                    survey.subsidy.refuses.first().reason
                    if survey.subsidy.refuses.first()
                    else "",
                    survey.investigator,
                    survey.reviewer,
                ]
                land_areas = factory.get_sliced_relation_generator(survey.farmer_id, 'land_areas')
                businesses = factory.get_sliced_relation_generator(survey.farmer_id, 'businesses')
                management_types = factory.get_sliced_relation_generator(survey.farmer_id, 'management_types')
                crop_marketings = factory.get_sliced_relation_generator(survey.farmer_id, 'crop_marketings')
                livestock_marketings = factory.get_sliced_relation_generator(survey.farmer_id, 'livestock_marketings')
                annual_incomes = factory.get_sliced_relation_generator(survey.farmer_id, 'annual_incomes')
                populations = factory.get_sliced_relation_generator(survey.farmer_id, 'populations')
                long_term_hires = factory.get_sliced_relation_generator(survey.farmer_id, 'long_term_hires')
                short_term_hires = factory.get_sliced_relation_generator(survey.farmer_id, 'short_term_hires')
                no_salary_hires = factory.get_sliced_relation_generator(survey.farmer_id, 'no_salary_hires')
                long_term_lacks = factory.get_sliced_relation_generator(survey.farmer_id, 'long_term_lacks')
                short_term_lacks = factory.get_sliced_relation_generator(survey.farmer_id, 'short_term_lacks')
                lacks = factory.get_sliced_relation_generator(survey.farmer_id, 'lacks')

                max_iter_count = max(factory.relation_count_mapping[survey.farmer_id].values())
                try:
                    for i in range(max_iter_count):
                        values1_ = values1 if i == 0 else [values1[0]] + [''] * (len(values1) - 1)
                        values2_ = values2 if i == 0 else [""] * len(values2)
                        row = (
                            values1_
                            + list(next(land_areas))
                            + list(next(businesses))
                            + list(next(management_types))
                            + list(next(crop_marketings))
                            + list(next(livestock_marketings))
                            + list(next(annual_incomes))
                            + list(next(populations))
                            + list(next(long_term_hires))
                            + list(next(short_term_hires))
                            + list(next(no_salary_hires))
                            + list(next(lacks))
                            + list(next(long_term_lacks))
                            + list(next(short_term_lacks))
                            + values2_
                        )
                        yield [output_formatter(item) for item in row]
                except Exception as e:
                    logger.exception(e)
                    errors.append(survey.farmer_id)
            if errors:
                yield ["未匯出成功的調查表:", ",".join(errors)]
            if not factory.check_exhausted():
                print('Something went wrong ... Relations not exhausted.')

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in row_generator()), content_type="text/csv"
        )
        response["Content-Disposition"] = 'attachment; filename="107_export.csv"'
        return response


class PhoneViewSet(StandardViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class AddressMatchViewSet(StandardViewSet):
    queryset = AddressMatch.objects.all()
    serializer_class = AddressMatchSerializer


class CityTownCodeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = CityTownCode.objects.all()
    serializer_class = CityTownCodeSerializer


class FarmLocationViewSet(StandardViewSet):
    queryset = FarmLocation.objects.all()
    serializer_class = FarmLocationSerializer


class LandStatusViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = LandStatus.objects.all()
    serializer_class = LandStatusSerializer


class LandTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer


class LandAreaViewSet(StandardViewSet):
    queryset = LandArea.objects.all()
    serializer_class = LandAreaSerializer


class BusinessViewSet(StandardViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class FarmRelatedBusinessViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = FarmRelatedBusiness.objects.all()
    serializer_class = FarmRelatedBusinessSerializer


class ManagementTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = ManagementType.objects.all()
    serializer_class = ManagementTypeSerializer


class CropMarketingViewSet(StandardViewSet):
    queryset = CropMarketing.objects.all()
    serializer_class = CropMarketingSerializer


class LivestockMarketingViewSet(StandardViewSet):
    queryset = LivestockMarketing.objects.all()
    serializer_class = LivestockMarketingSerializer


class ProductTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UnitViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class LossViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Loss.objects.all()
    serializer_class = LossSerializer


class ContractViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class AnnualIncomeViewSet(StandardViewSet):
    queryset = AnnualIncome.objects.all()
    serializer_class = AnnualIncomeSerializer


class MarketTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = MarketType.objects.all()
    serializer_class = MarketTypeSerializer


class IncomeRangeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = IncomeRange.objects.all()
    serializer_class = IncomeRangeSerializer


class AgeScopeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = AgeScope.objects.all()
    serializer_class = AgeScopeSerializer


class PopulationAgeViewSet(StandardViewSet):
    queryset = PopulationAge.objects.all()
    serializer_class = PopulationAgeSerializer


class PopulationViewSet(StandardViewSet):
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer


class RelationshipViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer


class GenderViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class EducationLevelViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class FarmerWorkDayViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = FarmerWorkDay.objects.all()
    serializer_class = FarmerWorkDaySerializer


class LifeStyleViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = LifeStyle.objects.all()
    serializer_class = LifeStyleSerializer


class LongTermHireViewSet(StandardViewSet):
    queryset = LongTermHire.objects.all()
    serializer_class = LongTermHireSerializer


class ShortTermHireViewSet(StandardViewSet):
    queryset = ShortTermHire.objects.all()
    serializer_class = ShortTermHireSerializer


class NoSalaryHireViewSet(StandardViewSet):
    queryset = NoSalaryHire.objects.all()
    serializer_class = NoSalaryHireSerializer


class NumberWorkersViewSet(StandardViewSet):
    queryset = NumberWorkers.objects.all()
    serializer_class = NumberWorkersSerializer


class LackViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Lack.objects.all()
    serializer_class = LackSerializer


class LongTermLackViewSet(StandardViewSet):
    queryset = LongTermLack.objects.all()
    serializer_class = LongTermLackSerializer


class ShortTermLackViewSet(StandardViewSet):
    queryset = ShortTermLack.objects.all()
    serializer_class = ShortTermLackSerializer


class WorkTypeViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class SubsidyViewSet(StandardViewSet):
    queryset = Subsidy.objects.all()
    serializer_class = SubsidySerializer


class RefuseViewSet(StandardViewSet):
    queryset = Refuse.objects.all()
    serializer_class = RefuseSerializer


class RefuseReasonViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = RefuseReason.objects.all()
    serializer_class = RefuseReasonSerializer


class MonthViewSet(ReadOnlyModelViewSet, StandardViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
