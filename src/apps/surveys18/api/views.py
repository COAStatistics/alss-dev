import json
import logging
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.exceptions import (
    ValidationError,
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework import pagination

from .serializers import SurveySerializer
from apps.surveys18.models import(
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
    Facility,
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

from . import serializers_singleton

review_logger = logging.getLogger('review')
system_logger = logging.getLogger('system')


class ThirtyPagination(pagination.PageNumberPagination):
    page_size = 30


class ThousandPagination(pagination.PageNumberPagination):
    page_size = 1000


class SurveyListAPIView(ListAPIView):
    serializer_class = SurveySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    pagination_class = ThirtyPagination
    search_fields = ['farmer_id']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Survey.objects.all()
        fid = self.request.GET.get('fid')
        readonly = json.loads(self.request.GET.get('readonly', 'false'))
        if fid:
            queryset_list = queryset_list.filter(
                    Q(farmer_id=fid) & Q(readonly=readonly)
                    ).distinct()
        return queryset_list


class SurveyUpdateAPIView(UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Survey.objects.get(id=pk)

    def patch(self, request):
        try:
            data = json.loads(request.data.get('data'))
            pk = data.get('id')
            survey = self.get_object(pk)
            serializer = SurveySerializer(survey,
                                          data=data,
                                          partial=True)  # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data=serializer.data)
            else:
                review_logger.error(serializer.errors, extra={
                    'object_id': pk,
                    'content_type': ContentType.objects.filter(app_label='surveys18', model='survey').first(),
                    'user': request.user,
                })
                raise ValidationError(serializer.errors)

        except Exception as e:
            system_logger.exception(e)
            return JsonResponse(data=e, safe=False)


# Serializer Singleton

class ContentTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ContentTypeSerializer
    queryset = ContentType.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            Q(app_label='surveys18', model='longtermhire') |
            Q(app_label='surveys18', model='shorttermhire')
        )


class SurveySingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.SurveySerializer
    queryset = Survey.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThirtyPagination


class ShortTermHireSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ShortTermHireSerializer
    queryset = ShortTermHire.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination

    search_fields = ['survey__id']

    def get_queryset(self, *args, **kwargs):
        survey_id = self.request.GET.get('survey_id')
        if survey_id:
            return self.queryset.filter(survey__id=survey_id)
        return self.queryset


class LongTermHireSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LongTermHireSerializer
    queryset = LongTermHire.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination

    search_fields = ['survey__id']

    def get_queryset(self, *args, **kwargs):
        survey_id = self.request.GET.get('survey_id')
        if survey_id:
            return self.queryset.filter(survey__id=survey_id)
        return self.queryset


class NumberWorkersSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.NumberWorkersSerializer
    queryset = NumberWorkers.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class ShortTermLackSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ShortTermLackSerializer
    queryset = ShortTermLack.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class LongTermLackSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LongTermLackSerializer
    queryset = LongTermLack.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class NoSalaryHireSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.NoSalaryHireSerializer
    queryset = NoSalaryHire.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class SubsidySingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.SubsidySerializer
    queryset = Subsidy.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class RefuseSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.RefuseSerializer
    queryset = Refuse.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class PopulationSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.PopulationSerializer
    queryset = Population.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class PopulationAgeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.PopulationAgeSerializer
    queryset = PopulationAge.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class CropMarketingSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.CropMarketingSerializer
    queryset = CropMarketing.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class LivestockMarketingSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LivestockMarketingSerializer
    queryset = LivestockMarketing.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class UnitSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.UnitSerializer
    queryset = Unit.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class ProductSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class BusinessSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.BusinessSerializer
    queryset = Business.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class LandTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LandTypeSerializer
    queryset = LandType.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class LandAreaSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LandAreaSerializer
    queryset = LandArea.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class PhoneSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.PhoneSerializer
    queryset = Phone.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class AddressMatchSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.AddressMatchSerializer
    queryset = AddressMatch.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


class AnnualIncomeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.AnnualIncomeSerializer
    queryset = AnnualIncome.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = ThousandPagination


# Sirializer Singleton No Pagination

class AgeScopeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.AgeScopeSerializer
    queryset = AgeScope.objects.all()
    permission_classes = [IsAuthenticated]


class WorkTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [IsAuthenticated]


class RefuseReasonSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.RefuseReasonSerializer
    queryset = RefuseReason.objects.all()
    permission_classes = [IsAuthenticated]


class FarmerWorkDaySingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.FarmerWorkDaySerializer
    queryset = FarmerWorkDay.objects.all()
    permission_classes = [IsAuthenticated]


class OtherFarmWorkSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.OtherFarmWorkSerializer
    queryset = OtherFarmWork.objects.all()
    permission_classes = [IsAuthenticated]


class RelationshipSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.RelationshipSerializer
    queryset = Relationship.objects.all()
    permission_classes = [IsAuthenticated]


class EducationLevelSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.EducationLevelSerializer
    queryset = EducationLevel.objects.all()
    permission_classes = [IsAuthenticated]


class LifeStyleSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LifeStyleSerializer
    queryset = LifeStyle.objects.all()
    permission_classes = [IsAuthenticated]


class GenderSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.GenderSerializer
    queryset = Gender.objects.all()
    permission_classes = [IsAuthenticated]


class LossSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LossSerializer
    queryset = Loss.objects.all()
    permission_classes = [IsAuthenticated]


class FacilitySingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.FacilitySerializer
    queryset = Facility.objects.all()
    permission_classes = [IsAuthenticated]


class ProductTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ProductTypeSerializer
    queryset = ProductType.objects.all()
    permission_classes = [IsAuthenticated]


class ContractSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]


class ManagementTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ManagementTypeSerializer
    queryset = ManagementType.objects.all()
    permission_classes = [IsAuthenticated]


class FarmRelatedBusinessSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.FarmRelatedBusinessSerializer
    queryset = FarmRelatedBusiness.objects.all()
    permission_classes = [IsAuthenticated]


class LandStatusSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LandStatusSerializer
    queryset = LandStatus.objects.all()
    permission_classes = [IsAuthenticated]


class LackSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.LackSerializer
    queryset = Lack.objects.all()
    permission_classes = [IsAuthenticated]


class IncomeRangeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.IncomeRangeSerializer
    queryset = IncomeRange.objects.all()
    permission_classes = [IsAuthenticated]


class MarketTypeSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.MarketTypeSerializer
    queryset = MarketType.objects.all()
    permission_classes = [IsAuthenticated]


class MonthSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.MonthSerializer
    queryset = Month.objects.all()
    permission_classes = [IsAuthenticated]
