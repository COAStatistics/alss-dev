import json

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

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
    MonthSerializer
)


class ContentTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            Q(app_label='surveys18', model='longtermhire') |
            Q(app_label='surveys18', model='shorttermhire')
        )


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        fid = self.request.GET.get('fid')
        readonly = json.loads(self.request.GET.get('readonly', 'false'))
        queryset = self.queryset
        if fid:
            queryset = self.queryset.filter(Q(farmer_id=fid) & Q(readonly=readonly)).distinct()
        return queryset


class PhoneViewSet(ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [IsAuthenticated]


class AddressMatchViewSet(ModelViewSet):
    queryset = AddressMatch.objects.all()
    serializer_class = AddressMatchSerializer
    permission_classes = [IsAuthenticated]


class CityTownCodeViewSet(ReadOnlyModelViewSet):
    queryset = CityTownCode.objects.all()
    serializer_class = CityTownCodeSerializer
    permission_classes = [IsAuthenticated]


class FarmLocationViewSet(ModelViewSet):
    queryset = FarmLocation.objects.all()
    serializer_class = FarmLocationSerializer
    permission_classes = [IsAuthenticated]


class LandStatusViewSet(ReadOnlyModelViewSet):
    queryset = LandStatus.objects.all()
    serializer_class = LandStatusSerializer
    permission_classes = [IsAuthenticated]


class LandTypeViewSet(ReadOnlyModelViewSet):
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer
    permission_classes = [IsAuthenticated]


class LandAreaViewSet(ModelViewSet):
    queryset = LandArea.objects.all()
    serializer_class = LandAreaSerializer
    permission_classes = [IsAuthenticated]


class BusinessViewSet(ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]


class FarmRelatedBusinessViewSet(ReadOnlyModelViewSet):
    queryset = FarmRelatedBusiness.objects.all()
    serializer_class = FarmRelatedBusinessSerializer
    permission_classes = [IsAuthenticated]


class ManagementTypeViewSet(ReadOnlyModelViewSet):
    queryset = ManagementType.objects.all()
    serializer_class = ManagementTypeSerializer
    permission_classes = [IsAuthenticated]


class CropMarketingViewSet(ModelViewSet):
    queryset = CropMarketing.objects.all()
    serializer_class = CropMarketingSerializer
    permission_classes = [IsAuthenticated]


class LivestockMarketingViewSet(ModelViewSet):
    queryset = LivestockMarketing.objects.all()
    serializer_class = LivestockMarketingSerializer
    permission_classes = [IsAuthenticated]


class ProductTypeViewSet(ReadOnlyModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class UnitViewSet(ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]


class LossViewSet(ReadOnlyModelViewSet):
    queryset = Loss.objects.all()
    serializer_class = LossSerializer
    permission_classes = [IsAuthenticated]


class ContractViewSet(ReadOnlyModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]


class AnnualIncomeViewSet(ModelViewSet):
    queryset = AnnualIncome.objects.all()
    serializer_class = AnnualIncomeSerializer
    permission_classes = [IsAuthenticated]


class MarketTypeViewSet(ReadOnlyModelViewSet):
    queryset = MarketType.objects.all()
    serializer_class = MarketTypeSerializer
    permission_classes = [IsAuthenticated]


class IncomeRangeViewSet(ReadOnlyModelViewSet):
    queryset = IncomeRange.objects.all()
    serializer_class = IncomeRangeSerializer
    permission_classes = [IsAuthenticated]


class AgeScopeViewSet(ReadOnlyModelViewSet):
    queryset = AgeScope.objects.all()
    serializer_class = AgeScopeSerializer
    permission_classes = [IsAuthenticated]


class PopulationAgeViewSet(ModelViewSet):
    queryset = PopulationAge.objects.all()
    serializer_class = PopulationAgeSerializer
    permission_classes = [IsAuthenticated]


class PopulationViewSet(ModelViewSet):
    queryset = Population.objects.all()
    serializer_class = PopulationSerializer
    permission_classes = [IsAuthenticated]


class RelationshipViewSet(ReadOnlyModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [IsAuthenticated]


class GenderViewSet(ReadOnlyModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [IsAuthenticated]


class EducationLevelViewSet(ReadOnlyModelViewSet):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    permission_classes = [IsAuthenticated]


class FarmerWorkDayViewSet(ReadOnlyModelViewSet):
    queryset = FarmerWorkDay.objects.all()
    serializer_class = FarmerWorkDaySerializer
    permission_classes = [IsAuthenticated]


class LifeStyleViewSet(ReadOnlyModelViewSet):
    queryset = LifeStyle.objects.all()
    serializer_class = LifeStyleSerializer
    permission_classes = [IsAuthenticated]


class LongTermHireViewSet(ModelViewSet):
    queryset = LongTermHire.objects.all()
    serializer_class = LongTermHireSerializer
    permission_classes = [IsAuthenticated]


class ShortTermHireViewSet(ModelViewSet):
    queryset = ShortTermHire.objects.all()
    serializer_class = ShortTermHireSerializer
    permission_classes = [IsAuthenticated]


class NoSalaryHireViewSet(ModelViewSet):
    queryset = NoSalaryHire.objects.all()
    serializer_class = NoSalaryHireSerializer
    permission_classes = [IsAuthenticated]


class NumberWorkersViewSet(ModelViewSet):
    queryset = NumberWorkers.objects.all()
    serializer_class = NumberWorkersSerializer
    permission_classes = [IsAuthenticated]


class LackViewSet(ReadOnlyModelViewSet):
    queryset = Lack.objects.all()
    serializer_class = LackSerializer
    permission_classes = [IsAuthenticated]


class LongTermLackViewSet(ModelViewSet):
    queryset = LongTermLack.objects.all()
    serializer_class = LongTermLackSerializer
    permission_classes = [IsAuthenticated]


class ShortTermLackViewSet(ModelViewSet):
    queryset = ShortTermLack.objects.all()
    serializer_class = ShortTermLackSerializer
    permission_classes = [IsAuthenticated]


class WorkTypeViewSet(ReadOnlyModelViewSet):
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
    permission_classes = [IsAuthenticated]


class SubsidyViewSet(ModelViewSet):
    queryset = Subsidy.objects.all()
    serializer_class = SubsidySerializer
    permission_classes = [IsAuthenticated]


class RefuseViewSet(ModelViewSet):
    queryset = Refuse.objects.all()
    serializer_class = RefuseSerializer
    permission_classes = [IsAuthenticated]


class RefuseReasonViewSet(ReadOnlyModelViewSet):
    queryset = RefuseReason.objects.all()
    serializer_class = RefuseReasonSerializer
    permission_classes = [IsAuthenticated]


class MonthViewSet(ReadOnlyModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
    permission_classes = [IsAuthenticated]
