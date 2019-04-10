from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, IntegerField

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


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class PhoneSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Phone
        fields = "__all__"


class AddressMatchSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = AddressMatch
        fields = "__all__"
        extra_kwargs = {"survey": {"validators": []}}


class CityTownCodeSerializer(ModelSerializer):
    class Meta:
        model = CityTownCode
        fields = "__all__"


class FarmLocationSerializer(ModelSerializer):
    class Meta:
        model = FarmLocation
        fields = "__all__"


class LandStatusSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandStatus
        fields = "__all__"


class LandTypeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandType
        fields = "__all__"


class LandAreaSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LandArea
        fields = "__all__"


class BusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Business
        fields = "__all__"
        extra_kwargs = {"farm_related_business": {"validators": []}}


class FarmRelatedBusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = FarmRelatedBusiness
        fields = "__all__"


class ManagementTypeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ManagementType
        fields = "__all__"


class CropMarketingSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = CropMarketing
        fields = "__all__"


class LivestockMarketingSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LivestockMarketing
        fields = "__all__"


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class LossSerializer(ModelSerializer):
    class Meta:
        model = Loss
        fields = "__all__"


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class AnnualIncomeSerializer(ModelSerializer):
    class Meta:
        model = AnnualIncome
        fields = "__all__"


class MarketTypeSerializer(ModelSerializer):
    class Meta:
        model = MarketType
        fields = "__all__"


class IncomeRangeSerializer(ModelSerializer):
    class Meta:
        model = IncomeRange
        fields = "__all__"


class AgeScopeSerializer(ModelSerializer):
    class Meta:
        model = AgeScope
        fields = "__all__"


class PopulationAgeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = PopulationAge
        fields = "__all__"


class PopulationSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Population
        fields = "__all__"


class RelationshipSerializer(ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class EducationLevelSerializer(ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = "__all__"


class FarmerWorkDaySerializer(ModelSerializer):
    class Meta:
        model = FarmerWorkDay
        fields = "__all__"


class LifeStyleSerializer(ModelSerializer):
    class Meta:
        model = LifeStyle
        fields = "__all__"


class NumberWorkersSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = NumberWorkers
        fields = "__all__"


class LongTermHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    number_workers = NumberWorkersSerializer(many=True)

    class Meta:
        model = LongTermHire
        fields = "__all__"


class ShortTermHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    number_workers = NumberWorkersSerializer(many=True)

    class Meta:
        model = ShortTermHire
        fields = "__all__"


class NoSalaryHireSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = NoSalaryHire
        fields = "__all__"


class LackSerializer(ModelSerializer):
    class Meta:
        model = Lack
        fields = "__all__"


class LongTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LongTermLack
        fields = "__all__"


class ShortTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ShortTermLack
        fields = "__all__"


class WorkTypeSerializer(ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class RefuseSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Refuse
        fields = "__all__"
        extra_kwargs = {"reason": {"validators": []}}


class SubsidySerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    refuses = RefuseSerializer(many=True)

    class Meta:
        model = Subsidy
        fields = "__all__"
        extra_kwargs = {"survey": {"validators": []}}


class RefuseReasonSerializer(ModelSerializer):
    class Meta:
        model = RefuseReason
        fields = "__all__"


class MonthSerializer(ModelSerializer):
    class Meta:
        model = Month
        fields = "__all__"


class SurveySerializer(ModelSerializer):
    annual_incomes = AnnualIncomeSerializer(many=True)
    address_match = AddressMatchSerializer(required=False, allow_null=True)
    businesses = BusinessSerializer(many=True)
    phones = PhoneSerializer(many=True)
    land_areas = LandAreaSerializer(many=True)
    crop_marketings = CropMarketingSerializer(many=True)
    livestock_marketings = LivestockMarketingSerializer(many=True)
    population_ages = PopulationAgeSerializer(many=True)
    populations = PopulationSerializer(many=True)
    subsidy = SubsidySerializer(required=False, allow_null=True)
    long_term_hires = LongTermHireSerializer(many=True)
    short_term_hires = ShortTermHireSerializer(many=True)
    no_salary_hires = NoSalaryHireSerializer(many=True)
    long_term_lacks = LongTermLackSerializer(many=True)
    short_term_lacks = ShortTermLackSerializer(many=True)
    farm_location = FarmLocationSerializer(required=False, allow_null=True)

    class Meta:
        model = Survey
        fields = "__all__"
