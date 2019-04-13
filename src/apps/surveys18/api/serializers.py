from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import ModelSerializer, IntegerField
from apps.surveys18.models import (
    AnnualIncome,
    Survey,
    AddressMatch,
    Phone,
    LandArea,
    ManagementType,
    CropMarketing,
    LivestockMarketing,
    PopulationAge,
    Population,
    Subsidy,
    LongTermHire,
    ShortTermHire,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
    LandStatus,
    LandType,
    FarmRelatedBusiness,
    NumberWorkers,
    Business,
    Refuse,
    Product,
    Month,
    Unit,
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
    Lack,
    IncomeRange,
    MarketType,
)


class MarketTypeSerializer(ModelSerializer):
    class Meta:
        model = MarketType
        fields = "__all__"


class IncomeRangeSerializer(ModelSerializer):
    class Meta:
        model = IncomeRange
        fields = "__all__"


class LackSerializer(ModelSerializer):
    class Meta:
        model = Lack
        fields = "__all__"


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class ProductTypeSerializer(ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class LossSerializer(ModelSerializer):
    class Meta:
        model = Loss
        fields = "__all__"


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class LifeStyleSerializer(ModelSerializer):
    class Meta:
        model = LifeStyle
        fields = "__all__"


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class WorkTypeSerializer(ModelSerializer):
    class Meta:
        model = WorkType
        fields = "__all__"


class AgeScopeSerializer(ModelSerializer):
    class Meta:
        model = AgeScope
        fields = "__all__"


class RefuseReasonSerializer(ModelSerializer):
    class Meta:
        model = RefuseReason
        fields = "__all__"


class FarmerWorkDaySerializer(ModelSerializer):
    class Meta:
        model = FarmerWorkDay
        fields = "__all__"


class OtherFarmWorkSerializer(ModelSerializer):
    class Meta:
        model = OtherFarmWork
        fields = "__all__"


class RelationshipSerializer(ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"


class EducationLevelSerializer(ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = "__all__"


class AnnualIncomeSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = AnnualIncome
        fields = "__all__"


class AddressMatchSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = AddressMatch
        fields = "__all__"
        extra_kwargs = {"survey": {"validators": []}}


class PhoneSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Phone
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


class NumberWorkersSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = NumberWorkers
        fields = "__all__"


class MonthSerializer(ModelSerializer):
    class Meta:
        model = Month
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


class ShortTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ShortTermLack
        fields = "__all__"


class LongTermLackSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = LongTermLack
        fields = "__all__"


class FarmRelatedBusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = FarmRelatedBusiness
        fields = "__all__"


class BusinessSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = Business
        fields = "__all__"
        extra_kwargs = {"farm_related_business": {"validators": []}}


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

    class Meta:
        model = Survey
        fields = "__all__"

    def update(self, instance, validated_data):
        # Update the instance
        instance.farmer_name = validated_data["farmer_name"]
        instance.note = validated_data["note"]
        instance.hire = validated_data["hire"]
        instance.non_hire = validated_data["non_hire"]

        instance.save()

        """Phone"""
        phone_ids = [item["id"] for item in validated_data["phones"] if "id" in item]
        # Delete not included in the request
        for obj in instance.phones.all():
            if obj.id not in phone_ids:
                obj.delete()
        for item in validated_data["phones"]:
            if "id" in item.keys():
                # Update included in the request
                phone_qs = instance.phones.filter(id=item["id"])
                if phone_qs:
                    phone_qs.update(phone=item["phone"] if "phone" in item else None)
            else:
                # Create
                Phone.objects.create(
                    survey=instance, phone=item["phone"] if "phone" in item else None
                )

        """Lack"""
        lack_ids = [item.id for item in validated_data["lacks"]]
        # Delete not included in the request
        for obj in instance.lacks.all():
            if obj.id not in lack_ids:
                instance.lacks.remove(obj)
        for obj in validated_data["lacks"]:
            if obj.id not in instance.lacks.values_list("id", flat=True):
                instance.lacks.add(obj)

        """AddressMatch"""
        if validated_data["address_match"]:
            instance.address_match.match = validated_data["address_match"]["match"]
            instance.address_match.mismatch = validated_data["address_match"][
                "mismatch"
            ]
            instance.address_match.address = validated_data["address_match"]["address"]
            instance.address_match.save()

        """LandArea"""
        land_area_ids = [
            item["id"] for item in validated_data["land_areas"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.land_areas.all():
            if obj.id not in land_area_ids:
                obj.delete()
        for item in validated_data["land_areas"]:
            if "id" in item.keys():
                # Update included in the request
                land_area_qs = instance.land_areas.filter(id=item["id"])
                if land_area_qs:
                    land_area_qs.update(
                        value=item["value"] if "value" in item else None,
                        type=item["type"] if "type" in item else None,
                        status=item["status"] if "status" in item else None,
                    )
            else:
                # Create
                LandArea.objects.create(
                    survey=instance,
                    value=item["value"] if "value" in item else None,
                    type=item["type"] if "type" in item else None,
                    status=item["status"] if "status" in item else None,
                )

        """Business"""
        business_ids = [
            item["id"] for item in validated_data["businesses"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.businesses.all():
            if obj.id not in business_ids:
                obj.delete()
        for item in validated_data["businesses"]:
            if "id" in item.keys():
                # Update included in the request
                business_qs = instance.businesses.filter(id=item["id"])
                if business_qs:
                    business_qs.update(extra=item["extra"] if "extra" in item else None)
            else:
                # Create
                Business.objects.create(
                    survey=instance,
                    extra=item["extra"] if "extra" in item else None,
                    farm_related_business=item["farm_related_business"]
                    if "farm_related_business" in item
                    else None,
                )

        """ManagementType"""
        management_type_ids = [item.id for item in validated_data["management_types"]]
        # Delete not included in the request
        for obj in instance.management_types.all():
            if obj.id not in management_type_ids:
                instance.management_types.remove(obj)
        for obj in validated_data["management_types"]:
            if obj.id not in instance.management_types.values_list("id", flat=True):
                instance.management_types.add(obj)

        """CropMarketing"""
        crop_marketing_ids = [
            item["id"] for item in validated_data["crop_marketings"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.crop_marketings.all():
            if obj.id not in crop_marketing_ids:
                obj.delete()
        for item in validated_data["crop_marketings"]:
            if "id" in item.keys():
                # Update included in the request
                crop_marketing_qs = instance.crop_marketings.filter(id=item["id"])
                if crop_marketing_qs:
                    crop_marketing_qs.update(
                        product=item["product"] if "product" in item else None,
                        loss=item["loss"] if "loss" in item else None,
                        unit=item["unit"] if "unit" in item else None,
                        land_number=item["land_number"]
                        if "land_number" in item
                        else None,
                        land_area=item["land_area"] if "land_area" in item else None,
                        plant_times=item["plant_times"]
                        if "plant_times" in item
                        else None,
                        total_yield=item["total_yield"]
                        if "total_yield" in item
                        else None,
                        unit_price=item["unit_price"] if "unit_price" in item else None,
                        has_facility=item["has_facility"]
                        if "has_facility" in item
                        else None,
                    )
            else:
                # Create
                CropMarketing.objects.create(
                    survey=instance,
                    product=item["product"] if "product" in item else None,
                    loss=item["loss"] if "loss" in item else None,
                    unit=item["unit"] if "unit" in item else None,
                    land_number=item["land_number"] if "land_number" in item else None,
                    land_area=item["land_area"] if "land_area" in item else None,
                    plant_times=item["plant_times"] if "plant_times" in item else None,
                    total_yield=item["total_yield"] if "total_yield" in item else None,
                    unit_price=item["unit_price"] if "unit_price" in item else None,
                    has_facility=item["has_facility"]
                    if "has_facility" in item
                    else None,
                )

        """LivestockMarketing"""
        livestock_marketing_ids = [
            item["id"]
            for item in validated_data["livestock_marketings"]
            if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.livestock_marketings.all():
            if obj.id not in livestock_marketing_ids:
                obj.delete()
        for item in validated_data["livestock_marketings"]:
            if "id" in item.keys():
                # Update included in the request
                livestock_marketing_qs = instance.livestock_marketings.filter(
                    id=item["id"]
                )
                if livestock_marketing_qs:
                    livestock_marketing_qs.update(
                        product=item["product"] if "product" in item else None,
                        loss=item["loss"] if "loss" in item else None,
                        unit=item["unit"] if "unit" in item else None,
                        raising_number=item["raising_number"]
                        if "raising_number" in item
                        else None,
                        total_yield=item["total_yield"]
                        if "total_yield" in item
                        else None,
                        unit_price=item["unit_price"] if "unit_price" in item else None,
                        contract=item["contract"] if "contract" in item else None,
                    )
            else:
                # Create
                LivestockMarketing.objects.create(
                    survey=instance,
                    product=item["product"] if "product" in item else None,
                    loss=item["loss"] if "loss" in item else None,
                    unit=item["unit"] if "unit" in item else None,
                    raising_number=item["raising_number"]
                    if "raising_number" in item
                    else None,
                    total_yield=item["total_yield"] if "total_yield" in item else None,
                    unit_price=item["unit_price"] if "unit_price" in item else None,
                    contract=item["contract"] if "contract" in item else None,
                )

        """AnnualIncome"""
        annual_income_ids = [
            item["id"] for item in validated_data["annual_incomes"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.annual_incomes.all():
            if obj.id not in annual_income_ids:
                obj.delete()
        for item in validated_data["annual_incomes"]:
            if "id" in item.keys():
                # Update included in the request
                annual_income_qs = instance.annual_incomes.filter(id=item["id"])
                if annual_income_qs:
                    annual_income_qs.update(
                        market_type=item["market_type"]
                        if "market_type" in item
                        else None,
                        income_range=item["income_range"]
                        if "income_range" in item
                        else None,
                    )
            else:
                # Create
                AnnualIncome.objects.create(
                    survey=instance,
                    market_type=item["market_type"] if "market_type" in item else None,
                    income_range=item["income_range"]
                    if "income_range" in item
                    else None,
                )

        """PopulationAge"""
        population_age_ids = [
            item["id"] for item in validated_data["population_ages"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.population_ages.all():
            if obj.id not in population_age_ids:
                obj.delete()
        for item in validated_data["population_ages"]:
            if "id" in item.keys():
                # Update included in the request
                population_age_qs = instance.population_ages.filter(id=item["id"])
                if population_age_qs:
                    population_age_qs.update(
                        count=item["count"] if "count" in item else None
                    )
            else:
                # Create
                PopulationAge.objects.create(
                    survey=instance,
                    count=item["count"] if "count" in item else None,
                    age_scope=item["age_scope"] if "age_scope" in item else None,
                    gender=item["gender"] if "gender" in item else None,
                )

        """Population"""
        population_ids = [
            item["id"] for item in validated_data["populations"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.populations.all():
            if obj.id not in population_ids:
                obj.delete()
        for item in validated_data["populations"]:
            if "id" in item.keys():
                # Update included in the request
                population_qs = instance.populations.filter(id=item["id"])
                if population_qs:
                    population_qs.update(
                        relationship=item["relationship"]
                        if "relationship" in item
                        else None,
                        gender=item["gender"] if "gender" in item else None,
                        birth_year=item["birth_year"] if "birth_year" in item else None,
                        education_level=item["education_level"]
                        if "education_level" in item
                        else None,
                        farmer_work_day=item["farmer_work_day"]
                        if "farmer_work_day" in item
                        else None,
                        life_style=item["life_style"] if "life_style" in item else None,
                        other_farm_work=item["other_farm_work"]
                        if "other_farm_work" in item
                        else None,
                    )
            else:
                # Create
                Population.objects.create(
                    survey=instance,
                    relationship=item["relationship"]
                    if "relationship" in item
                    else None,
                    gender=item["gender"] if "gender" in item else None,
                    birth_year=item["birth_year"] if "birth_year" in item else None,
                    education_level=item["education_level"]
                    if "education_level" in item
                    else None,
                    farmer_work_day=item["farmer_work_day"]
                    if "farmer_work_day" in item
                    else None,
                    life_style=item["life_style"] if "life_style" in item else None,
                    other_farm_work=item["other_farm_work"]
                    if "other_farm_work" in item
                    else None,
                )

        """LongTermHire"""
        long_term_hire_ids = [
            item["id"] for item in validated_data["long_term_hires"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.long_term_hires.all():
            if obj.id not in long_term_hire_ids:
                obj.delete()
        for item in validated_data["long_term_hires"]:
            if "id" in item.keys():
                # Update included in the request
                long_term_hire_qs = instance.long_term_hires.filter(id=item["id"])
                if long_term_hire_qs:
                    long_term_hire_qs.update(
                        work_type=item["work_type"] if "work_type" in item else None,
                        avg_work_day=item["avg_work_day"]
                        if "avg_work_day" in item
                        else None,
                    )
                    if "months" in item:
                        long_term_hire_qs.first().months.clear()
                        for month in item["months"]:
                            long_term_hire_qs.first().months.add(month)

                    """NumberWorker"""
                    number_worker_ids = [
                        item["id"] for item in item["number_workers"] if "id" in item
                    ]
                    # Delete not included in the request
                    for obj in long_term_hire_qs.first().number_workers.all():
                        if obj.id not in number_worker_ids:
                            obj.delete()
                    for obj in item["number_workers"]:
                        if "id" in obj.keys():
                            # Update included in the request
                            number_worker_qs = long_term_hire_qs.first().number_workers.filter(
                                id=obj["id"]
                            )
                            if number_worker_qs:
                                number_worker_qs.update(
                                    age_scope=obj["age_scope"]
                                    if "age_scope" in obj
                                    else None,
                                    count=obj["count"] if "count" in obj else None,
                                )
                        else:
                            # Create
                            NumberWorkers.objects.create(
                                age_scope=obj["age_scope"]
                                if "age_scope" in obj
                                else None,
                                count=obj["count"] if "count" in obj else None,
                                content_type=ContentType.objects.get(
                                    app_label="surveys18", model="longtermhire"
                                ),
                                object_id=item["id"],
                            )
            else:
                # Create
                content_object = LongTermHire.objects.create(
                    survey=instance,
                    work_type=item["work_type"] if "work_type" in item else None,
                    avg_work_day=item["avg_work_day"]
                    if "avg_work_day" in item
                    else None,
                )
                if "months" in item:
                    for month in item["months"]:
                        content_object.months.add(month)
                if "number_workers" in item:
                    for obj in item["number_workers"]:
                        NumberWorkers.objects.create(
                            age_scope=obj["age_scope"] if "age_scope" in obj else None,
                            count=obj["count"] if "count" in obj else None,
                            content_type=ContentType.objects.get(
                                app_label="surveys18", model="longtermhire"
                            ),
                            object_id=content_object.id,
                        )

        """ShortTermHire"""
        short_term_hire_ids = [
            item["id"] for item in validated_data["short_term_hires"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.short_term_hires.all():
            if obj.id not in short_term_hire_ids:
                obj.delete()
        for item in validated_data["short_term_hires"]:
            if "id" in item.keys():
                pass
                # Update included in the request
                short_term_hire_qs = instance.short_term_hires.filter(id=item["id"])
                if short_term_hire_qs:
                    short_term_hire_qs.update(
                        month=item["month"] if "month" in item else None,
                        avg_work_day=item["avg_work_day"]
                        if "avg_work_day" in item
                        else None,
                    )
                    if "work_types" in item:
                        short_term_hire_qs.first().work_types.clear()
                        for work_type in item["work_types"]:
                            short_term_hire_qs.first().work_types.add(work_type)

                    """NumberWorker"""
                    number_worker_ids = [
                        item["id"] for item in item["number_workers"] if "id" in item
                    ]
                    # Delete not included in the request
                    for obj in short_term_hire_qs.first().number_workers.all():
                        if obj.id not in number_worker_ids:
                            obj.delete()
                    for obj in item["number_workers"]:
                        if "id" in obj.keys():
                            # Update included in the request
                            number_worker_qs = short_term_hire_qs.first().number_workers.filter(
                                id=obj["id"]
                            )
                            if number_worker_qs:
                                number_worker_qs.update(
                                    age_scope=obj["age_scope"]
                                    if "age_scope" in obj
                                    else None,
                                    count=obj["count"] if "count" in obj else None,
                                )
                        else:
                            # Create
                            NumberWorkers.objects.create(
                                age_scope=obj["age_scope"]
                                if "age_scope" in obj
                                else None,
                                count=obj["count"] if "count" in obj else None,
                                content_type=ContentType.objects.get(
                                    app_label="surveys18", model="shorttermhire"
                                ),
                                object_id=item["id"],
                            )
            else:
                # Create
                content_object = ShortTermHire.objects.create(
                    survey=instance,
                    month=item["month"] if "month" in item else None,
                    avg_work_day=item["avg_work_day"]
                    if "avg_work_day" in item
                    else None,
                )
                if "work_types" in item:
                    for work_type in item["work_types"]:
                        content_object.work_types.add(work_type)
                if "number_workers" in item:
                    for obj in item["number_workers"]:
                        NumberWorkers.objects.create(
                            age_scope=obj["age_scope"] if "age_scope" in obj else None,
                            count=obj["count"] if "count" in obj else None,
                            content_type=ContentType.objects.get(
                                app_label="surveys18", model="shorttermhire"
                            ),
                            object_id=content_object.id,
                        )

        """NoSalaryHire"""
        no_salary_hire_ids = [
            item["id"] for item in validated_data["no_salary_hires"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.no_salary_hires.all():
            if obj.id not in no_salary_hire_ids:
                obj.delete()
        for item in validated_data["no_salary_hires"]:
            if "id" in item.keys():
                # Update included in the request
                no_salary_hire_qs = instance.no_salary_hires.filter(id=item["id"])
                if no_salary_hire_qs:
                    no_salary_hire_qs.update(
                        month=item["month"] if "month" in item else None,
                        count=item["count"] if "count" in item else None,
                    )
            else:
                # Create
                NoSalaryHire.objects.create(
                    survey=instance,
                    month=item["month"] if "month" in item else None,
                    count=item["count"] if "count" in item else None,
                )

        """LongTermLack"""
        long_term_lack_ids = [
            item["id"] for item in validated_data["long_term_lacks"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.long_term_lacks.all():
            if obj.id not in long_term_lack_ids:
                obj.delete()
        for item in validated_data["long_term_lacks"]:
            if "id" in item.keys():
                # Update included in the request
                long_term_lack_qs = instance.long_term_lacks.filter(id=item["id"])
                if long_term_lack_qs:
                    long_term_lack_qs.update(
                        work_type=item["work_type"] if "work_type" in item else None,
                        count=item["count"] if "count" in item else None,
                    )
                    if "months" in item:
                        long_term_lack_qs.first().months.clear()
                        for month in item["months"]:
                            long_term_lack_qs.first().months.add(month)
            else:
                # Create
                obj = LongTermLack.objects.create(
                    survey=instance,
                    work_type=item["work_type"] if "work_type" in item else None,
                    count=item["count"] if "count" in item else None,
                )
                if "months" in item:
                    for month in item["months"]:
                        obj.months.add(month)

        """ShortTermLack"""
        short_term_lack_ids = [
            item["id"] for item in validated_data["short_term_lacks"] if "id" in item
        ]
        # Delete not included in the request
        for obj in instance.short_term_lacks.all():
            if obj.id not in short_term_lack_ids:
                obj.delete()
        for item in validated_data["short_term_lacks"]:
            if "id" in item.keys():
                # Update included in the request
                short_term_lack_qs = instance.short_term_lacks.filter(id=item["id"])
                if short_term_lack_qs:
                    short_term_lack_qs.update(
                        product=item["product"] if "product" in item else None,
                        work_type=item["work_type"] if "work_type" in item else None,
                        count=item["count"] if "count" in item else None,
                    )
                    if "months" in item:
                        short_term_lack_qs.first().months.clear()
                        for month in item["months"]:
                            short_term_lack_qs.first().months.add(month)
            else:
                # Create
                obj = ShortTermLack.objects.create(
                    survey=instance,
                    product=item["product"] if "product" in item else None,
                    work_type=item["work_type"] if "work_type" in item else None,
                    count=item["count"] if "count" in item else None,
                )
                if "months" in item:
                    for month in item["months"]:
                        obj.months.add(month)

        """Subsidy"""
        if validated_data["subsidy"]:
            subsidy = validated_data["subsidy"]
            # Update
            instance.subsidy.has_subsidy = subsidy["has_subsidy"]
            instance.subsidy.none_subsidy = subsidy["none_subsidy"]
            instance.subsidy.month_delta = subsidy["month_delta"]
            instance.subsidy.day_delta = subsidy["day_delta"]
            instance.subsidy.hour_delta = subsidy["day_delta"]
            instance.subsidy.count = subsidy["count"]
            """Refuse"""
            refuse_ids = [item["id"] for item in subsidy["refuses"] if "id" in item]
            # Delete not included in the request
            for obj in instance.subsidy.refuses.all():
                if obj.id not in refuse_ids:
                    obj.delete()
            for item in subsidy["refuses"]:
                if "id" in item.keys():
                    # Update included in the request
                    refuse_qs = instance.subsidy.refuses.filter(id=item["id"])
                    if refuse_qs:
                        refuse_qs.update(
                            reason=item["reason"] if "reason" in item else None,
                            extra=item["extra"] if "extra" in item else None,
                        )
                else:
                    # Create
                    Refuse.objects.create(
                        subsidy=instance.subsidy,
                        reason=item["reason"] if "reason" in item else None,
                        extra=item["extra"] if "extra" in item else None,
                    )
            instance.subsidy.save()

        return instance
