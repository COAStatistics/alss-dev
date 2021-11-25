import json
import logging

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from config.viewsets import StandardViewSet
from apps.users.models import User
from apps.surveys18.tasks import async_export_106_statistics
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
    BuilderFile,
)

from . import serializers


logger = logging.getLogger("django.request")


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
            list(Survey.objects.filter(page=1).values_list("farmer_id", flat=True).distinct())
        )

        return context


class BuilderFileViewSet(StandardViewSet):
    queryset = BuilderFile.objects.all()
    serializer_class = serializers.BuilderFileSerializer

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


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["farmer_id"]

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

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

    @action(methods=["GET"], detail=False, serializer_class=serializers.SurveySimpleSerializer)
    def simple_list(self, request):
        return super().list(request)

    @action(methods=["PATCH"], detail=False)
    def patch(self, request):
        data = json.loads(request.data.get("data"))
        pk = data.get("id")
        try:
            survey = self.get_object(pk)
            serializer = serializers.SurveySerializer(
                survey, data=data, partial=True
            )  # set partial=True to update a data partially
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(data=serializer.data)
        except (ValidationError, Exception):
            logger.exception('Update survey data failed.', exc_info=True)
            raise

    @action(methods=["GET"], detail=False)
    def export_statistics(self, request):
        async_export_106_statistics.delay(request.user.email)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class ContentTypeViewSet(StandardViewSet):
    serializer_class = serializers.ContentTypeSerializer
    queryset = ContentType.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            Q(app_label="surveys18", model="longtermhire")
            | Q(app_label="surveys18", model="shorttermhire")
        )


class ShortTermHireViewSet(StandardViewSet):
    serializer_class = serializers.ShortTermHireSerializer
    queryset = ShortTermHire.objects.all()


class LongTermHireViewSet(StandardViewSet):
    serializer_class = serializers.LongTermHireSerializer
    queryset = LongTermHire.objects.all()


class NumberWorkersViewSet(StandardViewSet):
    serializer_class = serializers.NumberWorkersSerializer
    queryset = NumberWorkers.objects.all()


class ShortTermLackViewSet(StandardViewSet):
    serializer_class = serializers.ShortTermLackSerializer
    queryset = ShortTermLack.objects.all()


class LongTermLackViewSet(StandardViewSet):
    serializer_class = serializers.LongTermLackSerializer
    queryset = LongTermLack.objects.all()


class NoSalaryHireViewSet(StandardViewSet):
    serializer_class = serializers.NoSalaryHireSerializer
    queryset = NoSalaryHire.objects.all()


class SubsidyViewSet(StandardViewSet):
    serializer_class = serializers.SubsidySerializer
    queryset = Subsidy.objects.all()


class RefuseViewSet(StandardViewSet):
    serializer_class = serializers.RefuseSerializer
    queryset = Refuse.objects.all()


class PopulationViewSet(StandardViewSet):
    serializer_class = serializers.PopulationSerializer
    queryset = Population.objects.all()


class PopulationAgeViewSet(StandardViewSet):
    serializer_class = serializers.PopulationAgeSerializer
    queryset = PopulationAge.objects.all()


class CropMarketingViewSet(StandardViewSet):
    serializer_class = serializers.CropMarketingSerializer
    queryset = CropMarketing.objects.all()


class LivestockMarketingViewSet(StandardViewSet):
    serializer_class = serializers.LivestockMarketingSerializer
    queryset = LivestockMarketing.objects.all()


class UnitViewSet(StandardViewSet):
    serializer_class = serializers.UnitSerializer
    queryset = Unit.objects.all()


class ProductViewSet(StandardViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()


class BusinessViewSet(StandardViewSet):
    serializer_class = serializers.BusinessSerializer
    queryset = Business.objects.all()


class LandTypeViewSet(StandardViewSet):
    serializer_class = serializers.LandTypeSerializer
    queryset = LandType.objects.all()


class LandAreaViewSet(StandardViewSet):
    serializer_class = serializers.LandAreaSerializer
    queryset = LandArea.objects.all()


class PhoneViewSet(StandardViewSet):
    serializer_class = serializers.PhoneSerializer
    queryset = Phone.objects.all()


class AddressMatchViewSet(StandardViewSet):
    serializer_class = serializers.AddressMatchSerializer
    queryset = AddressMatch.objects.all()


class AnnualIncomeViewSet(StandardViewSet):
    serializer_class = serializers.AnnualIncomeSerializer
    queryset = AnnualIncome.objects.all()


class AgeScopeViewSet(StandardViewSet):
    serializer_class = serializers.AgeScopeSerializer
    queryset = AgeScope.objects.all()


class WorkTypeViewSet(StandardViewSet):
    serializer_class = serializers.WorkTypeSerializer
    queryset = WorkType.objects.all()


class RefuseReasonViewSet(StandardViewSet):
    serializer_class = serializers.RefuseReasonSerializer
    queryset = RefuseReason.objects.all()


class FarmerWorkDayViewSet(StandardViewSet):
    serializer_class = serializers.FarmerWorkDaySerializer
    queryset = FarmerWorkDay.objects.all()


class OtherFarmWorkViewSet(StandardViewSet):
    serializer_class = serializers.OtherFarmWorkSerializer
    queryset = OtherFarmWork.objects.all()


class RelationshipViewSet(StandardViewSet):
    serializer_class = serializers.RelationshipSerializer
    queryset = Relationship.objects.all()


class EducationLevelViewSet(StandardViewSet):
    serializer_class = serializers.EducationLevelSerializer
    queryset = EducationLevel.objects.all()


class LifeStyleViewSet(StandardViewSet):
    serializer_class = serializers.LifeStyleSerializer
    queryset = LifeStyle.objects.all()


class GenderViewSet(StandardViewSet):
    serializer_class = serializers.GenderSerializer
    queryset = Gender.objects.all()


class LossViewSet(StandardViewSet):
    serializer_class = serializers.LossSerializer
    queryset = Loss.objects.all()


class ProductTypeViewSet(StandardViewSet):
    serializer_class = serializers.ProductTypeSerializer
    queryset = ProductType.objects.all()


class ContractViewSet(StandardViewSet):
    serializer_class = serializers.ContractSerializer
    queryset = Contract.objects.all()


class ManagementTypeViewSet(StandardViewSet):
    serializer_class = serializers.ManagementTypeSerializer
    queryset = ManagementType.objects.all()


class FarmRelatedBusinessViewSet(StandardViewSet):
    serializer_class = serializers.FarmRelatedBusinessSerializer
    queryset = FarmRelatedBusiness.objects.all()


class LandStatusViewSet(StandardViewSet):
    serializer_class = serializers.LandStatusSerializer
    queryset = LandStatus.objects.all()


class LackViewSet(StandardViewSet):
    serializer_class = serializers.LackSerializer
    queryset = Lack.objects.all()


class IncomeRangeViewSet(StandardViewSet):
    serializer_class = serializers.IncomeRangeSerializer
    queryset = IncomeRange.objects.all()


class MarketTypeViewSet(StandardViewSet):
    serializer_class = serializers.MarketTypeSerializer
    queryset = MarketType.objects.all()


class MonthViewSet(StandardViewSet):
    serializer_class = serializers.MonthSerializer
    queryset = Month.objects.all()
