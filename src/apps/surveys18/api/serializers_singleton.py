from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.surveys18 import models


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Survey
        fields = '__all__'


class ShortTermHireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShortTermHire
        fields = '__all__'


class LongTermHireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LongTermHire
        fields = '__all__'


class NumberWorkersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberWorkers
        fields = '__all__'


class ShortTermLackSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShortTermLack
        fields = '__all__'


class LongTermLackSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LongTermLack
        fields = '__all__'


class NoSalaryHireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NoSalaryHire
        fields = '__all__'


class SubsidySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subsidy
        fields = '__all__'


class RefuseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Refuse
        fields = '__all__'


class PopulationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Population
        fields = '__all__'


class PopulationAgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PopulationAge
        fields = '__all__'


class CropMarketingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CropMarketing
        fields = '__all__'


class LivestockMarketingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LivestockMarketing
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Unit
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Business
        fields = '__all__'


class LandTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LandType
        fields = '__all__'


class LandAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LandArea
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = '__all__'


class AddressMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AddressMatch
        fields = '__all__'


class AnnualIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnnualIncome
        fields = '__all__'


# No Pagination

class AgeScopeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AgeScope
        fields = '__all__'


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkType
        fields = '__all__'


class RefuseReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RefuseReason
        fields = '__all__'


class FarmerWorkDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FarmerWorkDay
        fields = '__all__'


class OtherFarmWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OtherFarmWork
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Relationship
        fields = '__all__'


class EducationLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EducationLevel
        fields = '__all__'


class LifeStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LifeStyle
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gender
        fields = '__all__'


class LossSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loss
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Facility
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductType
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contract
        fields = '__all__'


class ManagementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ManagementType
        fields = '__all__'


class FarmRelatedBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FarmRelatedBusiness
        fields = '__all__'


class LandStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LandStatus
        fields = '__all__'


class LackSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lack
        fields = '__all__'


class IncomeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IncomeRange
        fields = '__all__'


class MarketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MarketType
        fields = '__all__'


class MonthSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Month
        fields = '__all__'
