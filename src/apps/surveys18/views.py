import json

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.exceptions import ValidationError

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from apps.surveys18.models import (
    Survey,
    ShortTermHire,
    LongTermHire,
    NumberWorkers,
    ShortTermLack,
    LongTermLack,
    NoSalaryHire,
    Subsidy,
    Refuse,
    Population,
    PopulationAge,
    CropMarketing,
    LivestockMarketing,
    Unit,
    Product,
    Business,
    LandType,
    LandArea,
    Phone,
    AddressMatch,
    AnnualIncome,
    AgeScope,
    WorkType,
    RefuseReason,
    FarmerWorkDay,
    OtherFarmWork,
    Relationship,
    EducationLevel,
    LifeStyle,
    Gender,
    Loss,
    ProductType,
    Contract,
    ManagementType,
    FarmRelatedBusiness,
    LandStatus,
    Lack,
    IncomeRange,
    MarketType,
    Month,
)

from . import serializers


class Surveys2018Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "surveys18/index.html"

    def get_context_data(self, **kwargs):
        context = super(Surveys2018Index, self).get_context_data(**kwargs)
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
        context["other_farm_works"] = OtherFarmWork.objects.all()
        context["relationships"] = Relationship.objects.all()
        context["life_styles"] = LifeStyle.objects.all()
        context["work_types"] = WorkType.objects.all()
        context["refuse_reasons"] = RefuseReason.objects.all()

        # ui elements
        ui = {
            "cropmarketing": render_to_string(
                "surveys18/row-ui/crop-marketing.html", context
            ),
            "livestockmarketing": render_to_string(
                "surveys18/row-ui/livestock-marketing.html", context
            ),
            "population": render_to_string("surveys18/row-ui/population.html", context),
            "longtermhire": render_to_string(
                "surveys18/row-ui/long-term-hire.html", context
            ),
            "longtermlack": render_to_string(
                "surveys18/row-ui/long-term-lack.html", context
            ),
            "shorttermhire": render_to_string(
                "surveys18/row-ui/short-term-hire.html", context
            ),
            "shorttermlack": render_to_string(
                "surveys18/row-ui/short-term-lack.html", context
            ),
            "nosalaryhire": render_to_string(
                "surveys18/row-ui/no-salary-hire.html", context
            ),
        }
        context["ui"] = json.dumps(ui)
        context["fid"] = json.dumps(
            list(Survey.objects.values_list("farmer_id", flat=True).distinct())
        )

        return context


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ["farmer_id"]

    def get_queryset(self, *args, **kwargs):
        fid = self.request.GET.get("fid")
        readonly = json.loads(self.request.GET.get("readonly", "false"))
        queryset = self.queryset
        if fid:
            queryset = queryset.filter(
                Q(farmer_id=fid) & Q(readonly=readonly)
            ).distinct()
        return queryset

    def get_object(self, pk):
        return Survey.objects.get(id=pk)

    @action(methods=["PATCH"], detail=False)
    def patch(self, request):
        try:
            data = json.loads(request.data.get("data"))
            pk = data.get("id")
            survey = self.get_object(pk)
            serializer = serializers.SurveySerializer(
                survey, data=data, partial=True
            )  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data)
            else:
                raise ValidationError(serializer.errors)

        except Exception as e:
            return JsonResponse(data=e, safe=False)


class ContentTypeViewSet(ModelViewSet):
    serializer_class = serializers.ContentTypeSerializer
    queryset = ContentType.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            Q(app_label="surveys18", model="longtermhire")
            | Q(app_label="surveys18", model="shorttermhire")
        )


class ShortTermHireViewSet(ModelViewSet):
    serializer_class = serializers.ShortTermHireSerializer
    queryset = ShortTermHire.objects.all()
    permission_classes = [IsAuthenticated]


class LongTermHireViewSet(ModelViewSet):
    serializer_class = serializers.LongTermHireSerializer
    queryset = LongTermHire.objects.all()
    permission_classes = [IsAuthenticated]


class NumberWorkersViewSet(ModelViewSet):
    serializer_class = serializers.NumberWorkersSerializer
    queryset = NumberWorkers.objects.all()
    permission_classes = [IsAuthenticated]


class ShortTermLackViewSet(ModelViewSet):
    serializer_class = serializers.ShortTermLackSerializer
    queryset = ShortTermLack.objects.all()
    permission_classes = [IsAuthenticated]


class LongTermLackViewSet(ModelViewSet):
    serializer_class = serializers.LongTermLackSerializer
    queryset = LongTermLack.objects.all()
    permission_classes = [IsAuthenticated]


class NoSalaryHireViewSet(ModelViewSet):
    serializer_class = serializers.NoSalaryHireSerializer
    queryset = NoSalaryHire.objects.all()
    permission_classes = [IsAuthenticated]


class SubsidyViewSet(ModelViewSet):
    serializer_class = serializers.SubsidySerializer
    queryset = Subsidy.objects.all()
    permission_classes = [IsAuthenticated]


class RefuseViewSet(ModelViewSet):
    serializer_class = serializers.RefuseSerializer
    queryset = Refuse.objects.all()
    permission_classes = [IsAuthenticated]


class PopulationViewSet(ModelViewSet):
    serializer_class = serializers.PopulationSerializer
    queryset = Population.objects.all()
    permission_classes = [IsAuthenticated]


class PopulationAgeViewSet(ModelViewSet):
    serializer_class = serializers.PopulationAgeSerializer
    queryset = PopulationAge.objects.all()
    permission_classes = [IsAuthenticated]


class CropMarketingViewSet(ModelViewSet):
    serializer_class = serializers.CropMarketingSerializer
    queryset = CropMarketing.objects.all()
    permission_classes = [IsAuthenticated]


class LivestockMarketingViewSet(ModelViewSet):
    serializer_class = serializers.LivestockMarketingSerializer
    queryset = LivestockMarketing.objects.all()
    permission_classes = [IsAuthenticated]


class UnitViewSet(ModelViewSet):
    serializer_class = serializers.UnitSerializer
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticated]


class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class BusinessViewSet(ModelViewSet):
    serializer_class = serializers.BusinessSerializer
    queryset = Business.objects.all()
    permission_classes = [IsAuthenticated]


class LandTypeViewSet(ModelViewSet):
    serializer_class = serializers.LandTypeSerializer
    queryset = LandType.objects.all()
    permission_classes = [IsAuthenticated]


class LandAreaViewSet(ModelViewSet):
    serializer_class = serializers.LandAreaSerializer
    queryset = LandArea.objects.all()
    permission_classes = [IsAuthenticated]


class PhoneViewSet(ModelViewSet):
    serializer_class = serializers.PhoneSerializer
    queryset = Phone.objects.all()
    permission_classes = [IsAuthenticated]


class AddressMatchViewSet(ModelViewSet):
    serializer_class = serializers.AddressMatchSerializer
    queryset = AddressMatch.objects.all()
    permission_classes = [IsAuthenticated]


class AnnualIncomeViewSet(ModelViewSet):
    serializer_class = serializers.AnnualIncomeSerializer
    queryset = AnnualIncome.objects.all()
    permission_classes = [IsAuthenticated]


class AgeScopeViewSet(ModelViewSet):
    serializer_class = serializers.AgeScopeSerializer
    queryset = AgeScope.objects.all()
    permission_classes = [IsAuthenticated]


class WorkTypeViewSet(ModelViewSet):
    serializer_class = serializers.WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [IsAuthenticated]


class RefuseReasonViewSet(ModelViewSet):
    serializer_class = serializers.RefuseReasonSerializer
    queryset = RefuseReason.objects.all()
    permission_classes = [IsAuthenticated]


class FarmerWorkDayViewSet(ModelViewSet):
    serializer_class = serializers.FarmerWorkDaySerializer
    queryset = FarmerWorkDay.objects.all()
    permission_classes = [IsAuthenticated]


class OtherFarmWorkViewSet(ModelViewSet):
    serializer_class = serializers.OtherFarmWorkSerializer
    queryset = OtherFarmWork.objects.all()
    permission_classes = [IsAuthenticated]


class RelationshipViewSet(ModelViewSet):
    serializer_class = serializers.RelationshipSerializer
    queryset = Relationship.objects.all()
    permission_classes = [IsAuthenticated]


class EducationLevelViewSet(ModelViewSet):
    serializer_class = serializers.EducationLevelSerializer
    queryset = EducationLevel.objects.all()
    permission_classes = [IsAuthenticated]


class LifeStyleViewSet(ModelViewSet):
    serializer_class = serializers.LifeStyleSerializer
    queryset = LifeStyle.objects.all()
    permission_classes = [IsAuthenticated]


class GenderViewSet(ModelViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()
    permission_classes = [IsAuthenticated]


class LossViewSet(ModelViewSet):
    serializer_class = serializers.LossSerializer
    queryset = Loss.objects.all()
    permission_classes = [IsAuthenticated]


class ProductTypeViewSet(ModelViewSet):
    serializer_class = serializers.ProductTypeSerializer
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticated]


class ContractViewSet(ModelViewSet):
    serializer_class = serializers.ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]


class ManagementTypeViewSet(ModelViewSet):
    serializer_class = serializers.ManagementTypeSerializer
    queryset = ManagementType.objects.all()
    permission_classes = [IsAuthenticated]


class FarmRelatedBusinessViewSet(ModelViewSet):
    serializer_class = serializers.FarmRelatedBusinessSerializer
    queryset = FarmRelatedBusiness.objects.all()
    permission_classes = [IsAuthenticated]


class LandStatusViewSet(ModelViewSet):
    serializer_class = serializers.LandStatusSerializer
    queryset = LandStatus.objects.all()
    permission_classes = [IsAuthenticated]


class LackViewSet(ModelViewSet):
    serializer_class = serializers.LackSerializer
    queryset = Lack.objects.all()
    permission_classes = [IsAuthenticated]


class IncomeRangeViewSet(ModelViewSet):
    serializer_class = serializers.IncomeRangeSerializer
    queryset = IncomeRange.objects.all()
    permission_classes = [IsAuthenticated]


class MarketTypeViewSet(ModelViewSet):
    serializer_class = serializers.MarketTypeSerializer
    queryset = MarketType.objects.all()
    permission_classes = [IsAuthenticated]


class MonthViewSet(ModelViewSet):
    serializer_class = serializers.MonthSerializer
    queryset = Month.objects.all()
    permission_classes = [IsAuthenticated]
