from django.conf import settings
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.utils.functional import cached_property
from django.db.models import Count, Max
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Model,
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    OneToOneField,
    ManyToManyField,
    IntegerField,
    BooleanField,
    TextField,
    DateField,
    PositiveIntegerField,
    FloatField,
    FileField,
    Q,
)
from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from apps.logs.models import ReviewLog


YES_NO_CHOICES = Choices((0, "No"), (1, "Yes"))

PRODUCT_TYPE_CHOICES = Choices((1, "crop", _("Crop")), (2, "animal", _("Animal")))

STRATIFY_WITH_CHOICES = Choices((1, "field", _("Field")), (2, "revenue", _("Revenue")))

REGION_CHOICES = Choices(
    (1, _("North")), (2, _("Central")), (3, _("South")), (4, _("East"))
)

NUMBER_WORKERS_CHOICES = Q(app_label="surveys20", model="longtermhire") | Q(
    app_label="surveys20", model="shorttermhire"
)


class Survey(Model):
    """
    read_only: Keep original data(read_only=True). Modify data(read_only=False).
    new field second and non_second table 1.4
    """

    farmer_id = CharField(max_length=12, verbose_name=_("Farmer Id"), db_index=True)
    farmer_name = CharField(
        null=True, blank=True, max_length=30, verbose_name=_("Name")
    )
    interviewee_relationship = CharField(
        null=True, blank=True, max_length=30, verbose_name=_("Interviewee Relationship")
    )
    total_pages = IntegerField(verbose_name=_("Total Pages"))
    page = IntegerField(verbose_name=_("Page"))
    origin_class = IntegerField(null=True, blank=True, verbose_name=_("Origin Class"))
    second = BooleanField(default=False, verbose_name=_("Second"))
    non_second = BooleanField(default=False, verbose_name=_("Non Second"))
    main_income_source = BooleanField(
        default=False, verbose_name=_("Main Income Source")
    )
    non_main_income_source = BooleanField(
        default=False, verbose_name=_("Non Main Income Source")
    )
    known_subsidy = BooleanField(default=False, verbose_name=_("Known Subsidy"))
    non_known_subsidy = BooleanField(default=False, verbose_name=_("Non Known Subsidy"))
    hire = BooleanField(default=False, verbose_name=_("Hire"))
    non_hire = BooleanField(default=False, verbose_name=_("Non Hire"))
    lacks = ManyToManyField(
        "surveys20.Lack", blank=True, related_name="surveys", verbose_name=_("Lack")
    )
    management_types = ManyToManyField(
        "surveys20.ManagementType",
        blank=True,
        related_name="surveys",
        verbose_name=_("Management Types"),
    )
    note = TextField(null=True, blank=True, verbose_name=_("Note"))
    readonly = BooleanField(default=True, verbose_name=_("Read Only"))

    investigator = CharField(
        null=True, blank=True, max_length=10, verbose_name=_("Investigator")
    )

    reviewer = CharField(
        null=True, blank=True, max_length=10, verbose_name=_("Reviewer")
    )

    date = DateField(null=True, blank=True, verbose_name=_("Investigation Date"))
    distance = IntegerField(
        null=True, blank=True, verbose_name=_("Investigation Distance(km)")
    )
    period = IntegerField(null=True, blank=True, verbose_name=_("Investigation Period"))

    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    review_logs = GenericRelation(ReviewLog, related_query_name="surveys20")

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Survey")

    def __str__(self):
        return self.farmer_id


class Phone(Model):
    """
    Contact phone number
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="phones",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    phone = CharField(max_length=100, null=True, blank=True, verbose_name=_("Phone"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phone")

    def __str__(self):
        return str(self.survey)


class AddressMatch(Model):
    """
    Contact address
    """

    survey = OneToOneField(
        "surveys20.Survey",
        related_name="address_match",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    match = BooleanField(default=False, verbose_name=_("Address Match"))
    mismatch = BooleanField(default=False, verbose_name=_("Address MisMatch"))
    address = CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Address")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("AddressMatch")
        verbose_name_plural = _("AddressMatch")

    def __str__(self):
        return str(self.survey)


class CityTownCode(Model):
    """
    New 107
    CityTown code
    Has yaml
    """

    city = CharField(max_length=20, null=True, blank=True, verbose_name=_("City"))
    town = CharField(max_length=20, null=True, blank=True, verbose_name=_("Town"))
    code = CharField(max_length=20, null=True, blank=True, verbose_name=_("Code"))
    region = PositiveIntegerField(
        null=True, blank=True, choices=REGION_CHOICES, verbose_name=_("Region")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("City")

    def __str__(self):
        return str(self.code)


class FarmLocation(Model):
    """
    New 107
    Check city town equal to code
    """

    survey = OneToOneField(
        "surveys20.Survey",
        related_name="farm_location",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    city = CharField(max_length=20, null=True, blank=True, verbose_name=_("City"))
    town = CharField(max_length=20, null=True, blank=True, verbose_name=_("Town"))
    code = ForeignKey(
        "surveys20.CityTownCode",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="farmlocation",
        verbose_name=_("Code"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("FarmLocation")
        verbose_name_plural = _("FarmLocation")
        ordering = ("id", "code")

    def __str__(self):
        return str(self.survey)


class LandStatus(Model):
    """
    Table 1.1
    Has yaml
    """

    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LandStatus")
        verbose_name_plural = _("LandStatus")

    def __str__(self):
        return self.name


class LandType(Model):
    """
    Table 1.1
    Has yaml
    """

    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    statuses = ManyToManyField(
        "surveys20.LandStatus",
        blank=True,
        related_name="land_type",
        verbose_name=_("Land Statuses"),
    )
    unit = ForeignKey(
        "surveys20.Unit",
        related_name="land_type",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Unit"),
    )
    has_land = BooleanField(default=True, verbose_name=_("Has Land"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LandType")
        verbose_name_plural = _("LandType")

    def __str__(self):
        return self.name


class LandArea(Model):
    """
    Table 1.1
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="land_areas",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    type = ForeignKey(
        "surveys20.LandType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="land_areas",
        verbose_name=_("Type"),
    )
    status = ForeignKey(
        "surveys20.LandStatus",
        related_name="land_areas",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Status"),
    )
    value = IntegerField(null=True, blank=True, verbose_name=_("Area Value"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LandArea")
        verbose_name_plural = _("LandArea")

    def __str__(self):
        return str(self.survey)


class Business(Model):
    """
    Table 1.2
    Survey data
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="businesses",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    farm_related_business = ForeignKey(
        "surveys20.FarmRelatedBusiness",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="business",
        verbose_name=_("Farm Related Business"),
    )
    extra = CharField(max_length=50, null=True, blank=True, verbose_name=_("Extra"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Business")

    def __str__(self):
        return str(self.survey)


class FarmRelatedBusiness(Model):
    """
    Table 1.2
    Option
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    has_extra = BooleanField(default=False, verbose_name=_("Has Extra"))
    has_business = BooleanField(default=True, verbose_name=_("Has Business"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("FarmRelatedBusiness")
        verbose_name_plural = _("FarmRelatedBusiness")

    def __str__(self):
        return str(self.name)


class ManagementType(Model):
    """
    Table 1.3
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=50, verbose_name=_("Name"))
    type = IntegerField(choices=PRODUCT_TYPE_CHOICES, verbose_name=_("Product Type"))
    stratify_with = IntegerField(
        choices=STRATIFY_WITH_CHOICES, verbose_name=_("Stratify With")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ManagementType")
        verbose_name_plural = _("ManagementType")

    def __str__(self):
        return str(self.name)


class CropMarketing(Model):
    """
    Changed 107
    Merge total_yield and unit_price to year_sales
    Add name field for product_name
    Table 1.5
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="crop_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys20.Product",
        related_name="products",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Product Code"),
    )
    loss = ForeignKey(
        "surveys20.Loss",
        related_name="crop_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys20.Unit",
        related_name="crop_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    name = CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Product Name")
    )
    land_number = IntegerField(null=True, blank=True, verbose_name=_("Land Number"))
    land_area = FloatField(null=True, blank=True, verbose_name=_("Land Area"))
    plant_times = IntegerField(null=True, blank=True, verbose_name=_("Plant Times"))
    year_sales = IntegerField(null=True, blank=True, verbose_name=_("Year Sales"))
    has_facility = IntegerField(
        null=True, blank=True, choices=YES_NO_CHOICES, verbose_name=_("Has Facility")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("CropMarketing")
        verbose_name_plural = _("CropMarketing")
        ordering = ("id", "land_number")

    def __str__(self):
        return str(self.survey)


class LivestockMarketing(Model):
    """
    Changed 107
    Merge total_yield and unit_price to year_sales
    Add name field for product_name
    Table 1.6
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="livestock_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys20.Product",
        related_name="livestock_marketing_product",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Product"),
    )
    loss = ForeignKey(
        "surveys20.Loss",
        related_name="livestock_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys20.Unit",
        related_name="livestock_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    contract = ForeignKey(
        "surveys20.Contract",
        related_name="contract",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Contract"),
    )
    name = CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Product Name")
    )
    raising_number = IntegerField(
        null=True, blank=True, verbose_name=_("Raising Number")
    )
    year_sales = IntegerField(null=True, blank=True, verbose_name=_("Year Sales"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LivestockMarketing")
        verbose_name_plural = _("LivestockMarketing")
        ordering = ("id",)

    def __str__(self):
        return str(self.survey)


class Product(Model):
    """
    Changed 107
    Table 1.5, 1.6
    Work hour between min_hour and max_hour for crop
    Display field hide children crop
    Display code at frontend page
    """

    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    code = CharField(max_length=50, verbose_name=_("Code"))
    min_hour = FloatField(null=True, blank=True, verbose_name=_("Min Hour"))
    max_hour = FloatField(null=True, blank=True, verbose_name=_("Max Hour"))
    parent = ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Parent Product"),
    )
    type = IntegerField(choices=PRODUCT_TYPE_CHOICES, verbose_name=_("Product Type"))
    management_type = ForeignKey(
        "surveys20.ManagementType",
        on_delete=CASCADE,
        verbose_name=_("Management Type"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Product")
        ordering = (
            "id",
            "code",
        )

    def __str__(self):
        return str(self.name)

    def display(self):
        return self.parent is None


class Unit(Model):
    """
    Table 1.5, 1.6
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    type = IntegerField(
        null=True,
        blank=True,
        choices=PRODUCT_TYPE_CHOICES,
        verbose_name=_("Product Type"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Unit")

    def __str__(self):
        return str(self.name)


class Loss(Model):
    """
    Table 1.5, 1.6
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    type = IntegerField(choices=PRODUCT_TYPE_CHOICES, verbose_name=_("Product Type"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Loss")
        verbose_name_plural = _("Loss")

    def __str__(self):
        return str(self.name)


class Contract(Model):
    """
    Table 1.6
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contract")

    def __str__(self):
        return str(self.name)


class AnnualIncome(Model):
    """
    Table 1.7
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="annual_incomes",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    market_type = ForeignKey(
        "surveys20.MarketType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Market Type"),
    )
    income_range = ForeignKey(
        "surveys20.IncomeRange",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Income Range"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("AnnualIncome")
        verbose_name_plural = _("AnnualIncomes")

    def __str__(self):
        return str(self.survey)


class MarketType(Model):
    """
    Table 1.7
    Has yaml
    """

    name = CharField(max_length=50, unique=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("MarketType")
        verbose_name_plural = _("MarketTypes")

    def __str__(self):
        return str(self.name)


class IncomeRange(Model):
    """
    Table 1.7
    Has yaml
    """

    name = CharField(max_length=50, unique=True, verbose_name=_("Name"))
    minimum = IntegerField(verbose_name=_("Minimum Income"))
    maximum = IntegerField(verbose_name=_("Maximum Income"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("IncomeRange")
        verbose_name_plural = _("IncomeRanges")

    def __str__(self):
        return self.name


class AgeScope(Model):
    """
    Table 2.1, 3.1.2, 3.1.3
    Has yaml
    """

    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    group = IntegerField(verbose_name=_("Group"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("AgeScope")
        verbose_name_plural = _("AgeScope")

    def __str__(self):
        return str(self.name)


class PopulationAge(Model):
    """
    Table 2.1
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="population_ages",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    gender = ForeignKey(
        "surveys20.Gender",
        verbose_name=_("Gender"),
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    age_scope = ForeignKey(
        "surveys20.AgeScope",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Age Scope"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Count"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("PopulationAge")
        verbose_name_plural = _("PopulationAge")

    def __str__(self):
        return str(self.survey)


class Population(Model):
    """
    Table 2.2
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="populations",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    relationship = ForeignKey(
        "surveys20.Relationship",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Relationship"),
    )
    gender = ForeignKey(
        "surveys20.Gender",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Gender"),
    )
    birth_year = IntegerField(null=True, blank=True, verbose_name=_("Birth Year"))
    education_level = ForeignKey(
        "surveys20.EducationLevel",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="education_level",
        verbose_name=_("Education Level"),
    )
    farmer_work_day = ForeignKey(
        "surveys20.FarmerWorkDay",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="farmer_work_day",
        verbose_name=_("Farmer Work Day"),
    )
    life_style = ForeignKey(
        "surveys20.LifeStyle",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="life_style",
        verbose_name=_("Life Style"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Population")
        verbose_name_plural = _("Population")
        ordering = ("id", "relationship")

    def __str__(self):
        return str(self.survey)


class Relationship(Model):
    """
    Table 2.2.2
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Relationship")
        verbose_name_plural = _("Relationship")

    def __str__(self):
        return str(self.name)


class Gender(Model):
    """
    Table 2.2.3
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Gender")
        verbose_name_plural = _("Gender")

    def __str__(self):
        return str(self.name)


class EducationLevel(Model):
    """
    Table 2.2.5
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    age = IntegerField(null=True, blank=True, verbose_name=_("Age"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("EducationLevel")
        verbose_name_plural = _("EducationLevel")

    def __str__(self):
        return str(self.name)


class FarmerWorkDay(Model):
    """
    Table 2.2.6
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    min_day = IntegerField(null=True, blank=True, verbose_name=_("Min Day"))
    max_day = IntegerField(null=True, blank=True, verbose_name=_("Max Day"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("FarmerWorkDay")
        verbose_name_plural = _("FarmerWorkDay")

    def __str__(self):
        return str(self.name)


class LifeStyle(Model):
    """
    Table 2.2.7
    Has yaml
    """

    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LifeStyle")
        verbose_name_plural = _("LifeStyle")

    def __str__(self):
        return str(self.name)


class LongTermHire(Model):
    """
    Table 3.1.2
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="long_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    work_type = ForeignKey(
        "surveys20.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_hires",
        verbose_name=_("Work Type"),
    )
    months = ManyToManyField(
        "surveys20.Month",
        blank=True,
        related_name="long_term_hires",
        verbose_name=_("Months"),
    )
    number_workers = GenericRelation(
        "surveys20.NumberWorkers", related_query_name="long_term_hires"
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LongTermHire")
        verbose_name_plural = _("LongTermHire")
        ordering = ("id",)

    def __str__(self):
        return str(self.survey)


class ShortTermHire(Model):
    """
    Table 3.1.3
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="short_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    month = ForeignKey(
        "surveys20.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    work_types = ManyToManyField(
        "surveys20.WorkType",
        blank=True,
        related_name="short_term_hires",
        verbose_name=_("Work Types"),
    )
    number_workers = GenericRelation(
        "surveys20.NumberWorkers", related_query_name="short_term_hires"
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ShortTermHire")
        verbose_name_plural = _("ShortTermHire")
        ordering = ("month",)

    def __str__(self):
        return str(self.survey)


class NoSalaryHire(Model):
    """
    Table 3.1.4
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="no_salary_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    month = ForeignKey(
        "surveys20.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("NoSalaryHire")
        verbose_name_plural = _("NoSalaryHire")
        ordering = ("month",)

    def __str__(self):
        return str(self.survey)


class NumberWorkers(Model):
    """
    Table 3.1.2, 3.1.3
    """

    content_type = ForeignKey(
        ContentType,
        limit_choices_to=NUMBER_WORKERS_CHOICES,
        on_delete=CASCADE,
        related_name="survey20_number_workers",
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    age_scope = ForeignKey(
        "surveys20.AgeScope",
        related_name="number_workers",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Age Scope"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Count"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("NumberWorkers")
        verbose_name_plural = _("NumberWorkers")

    def __str__(self):
        return str(self.content_object)


class Lack(Model):
    """
    Table 3.2.1
    Has yaml
    """

    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    is_lack = BooleanField(default=False, verbose_name=_("Is Lack"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Lack")
        verbose_name_plural = _("Lack")

    def __str__(self):
        return str(self.name)


class LongTermLack(Model):
    """
    Changed 107
    Add avg_lack_day field
    Table 3.2.2
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="long_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    work_type = ForeignKey(
        "surveys20.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_lacks",
        verbose_name=_("Work Type"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys20.Month",
        blank=True,
        related_name="long_term_lacks",
        verbose_name=_("Months"),
    )
    avg_lack_day = FloatField(null=True, blank=True, verbose_name=_("Average Lack Day"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("LongTermLack")
        verbose_name_plural = _("LongTermLack")

    def __str__(self):
        return str(self.survey)


class ShortTermLack(Model):
    """
    Changed 107
    Add avg_lack_day field
    Add name field for product name
    Table 3.2.3
    """

    survey = ForeignKey(
        "surveys20.Survey",
        related_name="short_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys20.Product",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="short_term_lacks",
        verbose_name=_("Product"),
    )
    work_type = ForeignKey(
        "surveys20.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="short_term_lacks",
        verbose_name=_("Work Type"),
    )
    name = CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Product Name")
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys20.Month",
        blank=True,
        related_name="short_term_lacks",
        verbose_name=_("Months"),
    )
    avg_lack_day = FloatField(null=True, blank=True, verbose_name=_("Average Lack Day"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ShortTermLack")
        verbose_name_plural = _("ShortTermLack")

    def __str__(self):
        return str(self.survey)


class WorkType(Model):
    """
    Table 3.1.2, 3.1.3, 3.2.2, 3.2.3
    Has yaml
    """

    code = IntegerField(null=True, blank=True, verbose_name=_("Code"))
    name = CharField(max_length=30, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("WorkType")
        verbose_name_plural = _("WorkType")

    def __str__(self):
        return str(self.name)


class Subsidy(Model):
    """
    Table 3.3.1 -> 3.3.2
    """

    survey = OneToOneField(
        "surveys20.Survey",
        related_name="subsidy",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    has_subsidy = BooleanField(default=False, verbose_name=_("Has Subsidy"))
    none_subsidy = BooleanField(default=False, verbose_name=_("None Subsidy"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Subsidy")
        verbose_name_plural = _("Subsidy")

    def __str__(self):
        return str(self.survey)


class Refuse(Model):
    """
    Table 3.3.2
    """

    subsidy = ForeignKey(
        "surveys20.Subsidy",
        related_name="refuses",
        on_delete=CASCADE,
        verbose_name=_("Subsidy"),
    )
    reason = ForeignKey(
        "surveys20.RefuseReason",
        related_name="refuse",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Refuse"),
    )
    extra = CharField(max_length=100, null=True, blank=True, verbose_name=_("Extra"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Refuse")
        verbose_name_plural = _("Refuse")

    def __str__(self):
        return str(self.reason)


class RefuseReason(Model):
    """
    Table 3.3.2
    Has yaml
    """

    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    has_extra = BooleanField(default=False, verbose_name=_("Has Extra"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("RefuseReason")
        verbose_name_plural = _("RefuseReason")

    def __str__(self):
        return str(self.name)


class Month(Model):
    """
    Has yaml
    """

    name = CharField(max_length=50, unique=True, verbose_name=_("Name"))
    value = IntegerField(choices=MONTHS.items())
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Month")
        verbose_name_plural = _("Month")

    def __str__(self):
        return str(self.name)


class BuilderFile(Model):
    create_time = DateTimeField(auto_now_add=True, verbose_name=_("Create Time"))
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="surveys20_files",
        verbose_name=_("User"),
    )
    token = TextField(null=True, blank=True, verbose_name=_("Token String"))
    datafile = FileField(
        null=True,
        blank=True,
        upload_to="surveys20/builders/",
        verbose_name=_("DataFile"),
    )
    delete_exist = BooleanField(default=False)

    class Meta:
        verbose_name = _("BuilderFile")
        verbose_name_plural = _("BuilderFile")

    def __str__(self):
        return str(self.user)


class Stratify(Model):
    """
    field=公畝;revenue=萬元
    """

    management_type = ForeignKey(
        "surveys20.ManagementType",
        on_delete=CASCADE,
        related_name="stratifies",
        verbose_name=_("Management Type"),
    )
    is_hire = BooleanField(verbose_name=_("Is Hire"))
    min_field = FloatField(null=True, blank=True, verbose_name=_("Min Field"))
    max_field = FloatField(null=True, blank=True, verbose_name=_("Max Field"))
    min_revenue = PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Min Revenue")
    )
    max_revenue = PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Max Revenue")
    )
    code = PositiveIntegerField(db_index=True, verbose_name=_("Code"))
    population = PositiveIntegerField(verbose_name=_("Population(Statistic)"))

    class Meta:
        verbose_name = _("Stratify")
        verbose_name_plural = _("Stratify")

    def __str__(self):
        return str(self.code)

    @property
    def sibling(self):
        import operator

        return Stratify.objects.get(
            management_type=self.management_type,
            min_field=self.min_field,
            max_field=self.max_field,
            min_revenue=self.min_revenue,
            max_revenue=self.max_revenue,
            is_hire=operator.not_(self.is_hire),
        )

    @cached_property
    def sample_count(self):
        return self.farmer_stats.count()

    @cached_property
    def magnification_factor(self):
        # 各層母體數 / 各層樣本數
        if self.sibling.sample_count == 0:
            # 檢查同一規模是否有樣本數，若無須併層
            return (self.population + self.sibling.population) / (
                self.sample_count + self.sibling.sample_count
            )
        return self.population / self.sample_count


class FarmerStat(Model):
    survey = OneToOneField(
        "surveys20.Survey",
        on_delete=CASCADE,
        related_name="farmer_stat",
        verbose_name=_("Survey"),
    )
    stratify = ForeignKey(
        "surveys20.Stratify",
        on_delete=CASCADE,
        related_name="farmer_stats",
        verbose_name=_("Stratify"),
    )
    create_time = AutoCreatedField(_("Create Time"))
    update_time = AutoLastModifiedField(_("Update Time"))

    class Meta:
        verbose_name = _("Farmer Stat")
        verbose_name_plural = _("Farmer Stat")

    def __str__(self):
        return str(self.survey)

    @classmethod
    @atomic
    def resolve_all(cls):
        # Filter surveys has valid management type
        valid_management_type_survey_ids = list(
            Survey.objects.annotate(m_count=Count("management_types"))
            .filter(m_count=1)
            .values_list("id", flat=True)
        )

        # Query surveys
        survey_qs = Survey.objects.exclude(note__icontains="無效戶").filter(
            readonly=False, page=1, id__in=valid_management_type_survey_ids
        )

        # Iter through surveys
        stats = []
        for survey in survey_qs:
            try:
                stratify = cls.get_stratify(survey)
                stats.append(
                    cls(
                        survey=survey,
                        stratify=stratify,
                    )
                )
            except Stratify.DoesNotExist:
                print(f"Cannot find stratify for survey {survey}.")

        # Bulk operation
        cls.objects.all().delete()
        cls.objects.bulk_create(stats)

    @staticmethod
    def get_stratify(survey: Survey):
        management_type = survey.management_types.first()
        survey_ids = Survey.objects.filter(
            readonly=False, farmer_id=survey.farmer_id
        ).values_list("id", flat=True)
        if management_type.stratify_with == STRATIFY_WITH_CHOICES.field:
            # 同一耕作地編號種植面積取最大值，不同耕作地編號種植面積加總
            land_areas = (
                CropMarketing.objects.filter(survey__id__in=survey_ids)
                .values("land_number")
                .order_by()
                .annotate(max_value=Max("land_area"))
            )
            total_area = sum(d["max_value"] for d in land_areas)
            return Stratify.objects.get(
                management_type=management_type,
                min_field__lte=total_area,
                max_field__gt=total_area,
                is_hire=survey.hire,
            )
        elif management_type.stratify_with == STRATIFY_WITH_CHOICES.revenue:
            # 取得銷售額總計區間
            annual_incomes = survey.annual_incomes.filter(market_type__id=5)
            if annual_incomes.count() == 1:
                income_range = annual_incomes.first().income_range
                avg = (income_range.minimum + income_range.maximum) / 2
                return Stratify.objects.get(
                    management_type=management_type,
                    min_revenue__lte=avg,
                    max_revenue__gte=avg,
                    is_hire=survey.hire,
                )
            else:
                raise ValueError(f"Survey {survey}'s annual income is missing.")
