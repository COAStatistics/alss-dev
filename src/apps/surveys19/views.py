import json
import logging
import csv

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from config.viewsets import StandardViewSet

from apps.users.models import User
from apps.surveys19.tasks import async_export_107, async_export_107_statistics
from apps.surveys19.export import SurveyRelationGeneratorFactory
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

from apps.surveys19.serializers import (
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

logger = logging.getLogger('django.request')


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
        permissions = [IsAdminUser]  # default
        if self.request.method == 'GET':
            permissions = [IsAuthenticated]
        if getattr(self, 'action'):
            if self.action == 'patch':
                permissions = [IsAuthenticated]
            if self.action == 'export':
                permissions = [IsAdminUser]
        return [permission() for permission in permissions]

    @action(methods=["GET"], detail=False, serializer_class=SurveySimpleSerializer)
    def simple_list(self, request):
        return super().list(request)

    @action(methods=["PATCH"], detail=False)
    def patch(self, request):
        data = json.loads(request.data.get("data"))
        pk = data.get("id")
        try:
            survey = self.get_object(pk)
            serializer = SurveySerializer(
                survey, data=data, partial=True
            )  # set partial=True to update a data partially
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(data=serializer.data)
        except (ValidationError, Exception):
            logger.exception('Update survey data failed.', exc_info=True)
            raise

    @action(methods=["GET"], detail=False)
    def export(self, request):
        """A view that streams a large CSV file."""
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet
        # applications.

        async_export_107.delay(request.user.email)
        return HttpResponse('ok')

    @action(methods=["GET"], detail=False)
    def export_statistics(self, request):
        async_export_107_statistics.delay(request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

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
