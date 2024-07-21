import operator
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

NUMBER_WORKERS_CHOICES = Q(app_label="surveys24", model="longtermhire") | Q(
    app_label="surveys24", model="shorttermhire"
)

MANAGEMENT_LEVEL = Choices(
    (1, "small", _("Small")), (2, "middle", _("Middle")), (3, "large", _("Large"))
)

FOREIGN_LABOR_HIRE_TYPE = Choices(
    (1, "long_term_labor", _("Long Term Labor")), (2, "short_term_labor", _("Short Term Labor"))
)

SAMPLE_GROUP = Choices(
    (1, "origin", _("Origin")), (2, "mix", _("Mix"))
)


class Survey(Model):
    """
    read_only: Keep original data(read_only=True). Modify data(read_only=False).
    removed fields: second and non_second table 1.4
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
    main_income_source = BooleanField(
        default=False, verbose_name=_("Main Income Source")
    )
    non_main_income_source = BooleanField(
        default=False, verbose_name=_("Non Main Income Source")
    )
    # TODO: known_subsidy, non_known_subsidy uses virtual property to decide. (in Subsidy)
    # Currently only stores the value from builder, not edited by UI.
    known_subsidy = BooleanField(default=False, verbose_name=_("Known Subsidy"))
    non_known_subsidy = BooleanField(default=False, verbose_name=_("Non Known Subsidy"))
    hire = BooleanField(default=False, verbose_name=_("Hire"))
    non_hire = BooleanField(default=False, verbose_name=_("Non Hire"))
    lacks = ManyToManyField(
        "surveys24.Lack", blank=True, related_name="surveys", verbose_name=_("Lack")
    )
    has_farm_outsource = BooleanField(default=False, verbose_name=_("Has Farm Outsource"))
    non_has_farm_outsource = BooleanField(default=False, verbose_name=_("Non Has Farm Outsource"))
    management_types = ManyToManyField(
        "surveys24.ManagementType",
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

    review_logs = GenericRelation(ReviewLog, related_query_name="surveys24")
    # new field add in 24
    is_invalid = BooleanField(default=False, verbose_name=_("Is Invalid"))
    invalid_reason = TextField(null=True, blank=True, verbose_name=_("Invalid Reason"))

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
        "surveys24.Survey",
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
        "surveys24.Survey",
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
        "surveys24.Survey",
        related_name="farm_location",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    city = CharField(max_length=20, null=True, blank=True, verbose_name=_("City"))
    town = CharField(max_length=20, null=True, blank=True, verbose_name=_("Town"))
    code = ForeignKey(
        "surveys24.CityTownCode",
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
        "surveys24.LandStatus",
        blank=True,
        related_name="land_type",
        verbose_name=_("Land Statuses"),
    )
    unit = ForeignKey(
        "surveys24.Unit",
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
        "surveys24.Survey",
        related_name="land_areas",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    type = ForeignKey(
        "surveys24.LandType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="land_areas",
        verbose_name=_("Type"),
    )
    status = ForeignKey(
        "surveys24.LandStatus",
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
        "surveys24.Survey",
        related_name="businesses",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    farm_related_business = ForeignKey(
        "surveys24.FarmRelatedBusiness",
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
        "surveys24.Survey",
        related_name="crop_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys24.Product",
        related_name="products",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Product Code"),
    )
    loss = ForeignKey(
        "surveys24.Loss",
        related_name="crop_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys24.Unit",
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
        "surveys24.Survey",
        related_name="livestock_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys24.Product",
        related_name="livestock_marketing_product",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Product"),
    )
    loss = ForeignKey(
        "surveys24.Loss",
        related_name="livestock_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys24.Unit",
        related_name="livestock_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    contract = ForeignKey(
        "surveys24.Contract",
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
        "surveys24.ManagementType",
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
        "surveys24.Survey",
        related_name="annual_incomes",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    market_type = ForeignKey(
        "surveys24.MarketType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Market Type"),
    )
    income_range = ForeignKey(
        "surveys24.IncomeRange",
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
        "surveys24.Survey",
        related_name="population_ages",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    gender = ForeignKey(
        "surveys24.Gender",
        verbose_name=_("Gender"),
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    age_scope = ForeignKey(
        "surveys24.AgeScope",
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
        "surveys24.Survey",
        related_name="populations",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    relationship = ForeignKey(
        "surveys24.Relationship",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Relationship"),
    )
    gender = ForeignKey(
        "surveys24.Gender",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Gender"),
    )
    birth_year = IntegerField(null=True, blank=True, verbose_name=_("Birth Year"))
    education_level = ForeignKey(
        "surveys24.EducationLevel",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="education_level",
        verbose_name=_("Education Level"),
    )
    farmer_work_day = ForeignKey(
        "surveys24.FarmerWorkDay",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="farmer_work_day",
        verbose_name=_("Farmer Work Day"),
    )
    life_style = ForeignKey(
        "surveys24.LifeStyle",
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
        "surveys24.Survey",
        related_name="long_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    work_type = ForeignKey(
        "surveys24.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_hires",
        verbose_name=_("Work Type"),
    )
    months = ManyToManyField(
        "surveys24.Month",
        blank=True,
        related_name="long_term_hires",
        verbose_name=_("Months"),
    )
    number_workers = GenericRelation(
        "surveys24.NumberWorkers", related_query_name="long_term_hires"
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
        "surveys24.Survey",
        related_name="short_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    month = ForeignKey(
        "surveys24.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    work_types = ManyToManyField(
        "surveys24.WorkType",
        blank=True,
        related_name="short_term_hires",
        verbose_name=_("Work Types"),
    )
    number_workers = GenericRelation(
        "surveys24.NumberWorkers", related_query_name="short_term_hires"
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
        "surveys24.Survey",
        related_name="no_salary_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    month = ForeignKey(
        "surveys24.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
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
        related_name="surveys24_number_workers",
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    age_scope = ForeignKey(
        "surveys24.AgeScope",
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
    Table 3.3.1
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
    Table 3.3.3
    """

    survey = ForeignKey(
        "surveys24.Survey",
        related_name="long_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    work_type = ForeignKey(
        "surveys24.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_lacks",
        verbose_name=_("Work Type"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys24.Month",
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
    Table 3.3.4
    """

    survey = ForeignKey(
        "surveys24.Survey",
        related_name="short_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys24.Product",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="short_term_lacks",
        verbose_name=_("Product"),
    )
    work_type = ForeignKey(
        "surveys24.WorkType",
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
        "surveys24.Month",
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
    Table 4
    New fields: heard_app, non_heard_app (3.3.2)
    Removed fields: has_subsidy, none_subsidy, heard_app, none_heard_app
    """

    survey = OneToOneField(
        "surveys24.Survey",
        related_name="subsidy",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
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

    @property
    def has_subsidy(self):
        return self.subsidy.applies.count() > 0

    @property
    def non_known_subsidy(self):
        # 沒聽過視為理由(reason)為0的沒申請(refuse)
        return self.refuses.filter(reason=0).count() > 0

    @property
    def known_subsidy(self):
        return self.refuses.exclude(reason=0).count() > 0 or self.has_subsidy


class ApplyMethod(Model):
    """
    (New table added in 23)
    Table 4.1
    Has yaml
    """

    name = CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ApplyMethod")
        verbose_name_plural = _("ApplyMethod")


class Apply(Model):
    """
    Table 4.1
    New field: method.
    """

    subsidy = ForeignKey(
        "surveys24.Subsidy",
        related_name="applies",
        on_delete=CASCADE,
        verbose_name=_("Subsidy"),
    )
    method = ForeignKey(
        "surveys24.ApplyMethod",
        related_name="apply",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ApplyMethod"),
    )
    result = ForeignKey(
        "surveys24.ApplyResult",
        related_name="apply",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ApplyResult"),
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Apply")
        verbose_name_plural = _("Apply")

    def __str__(self):
        return str(self.result)


class ApplyResult(Model):
    """
    Table 4.1
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
        verbose_name = _("ApplyResult")
        verbose_name_plural = _("ApplyResult")

    def __str__(self):
        return str(self.name)


class Refuse(Model):
    """
    Table 4.1
    New field: method.
    """

    subsidy = ForeignKey(
        "surveys24.Subsidy",
        related_name="refuses",
        on_delete=CASCADE,
        verbose_name=_("Subsidy"),
    )
    method = ForeignKey(
        "surveys24.ApplyMethod",
        related_name="refuse",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ApplyMethod"),
    )
    reason = ForeignKey(
        "surveys24.RefuseReason",
        related_name="refuse",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("RefuseReason"),
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
    Table 4.1
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
        related_name="surveys24_files",
        verbose_name=_("User"),
    )
    token = TextField(null=True, blank=True, verbose_name=_("Token String"))
    datafile = FileField(
        null=True,
        blank=True,
        upload_to="surveys24/builders/",
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
        "surveys24.ManagementType",
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
    # 110 新增，併層邏輯複雜化
    level = PositiveIntegerField(
        choices=MANAGEMENT_LEVEL, verbose_name=_("Management Level")
    )
    # 112 新增，區分高齡
    is_senility = BooleanField(null=True, blank=True, db_index=True, verbose_name=_("Is Senility"))

    class Meta:
        verbose_name = _("Stratify")
        verbose_name_plural = _("Stratify")

    def __str__(self):
        return str(self.code)

    @property
    def sibling(self):
        return Stratify.objects.get(
            management_type=self.management_type,
            min_field=self.min_field,
            max_field=self.max_field,
            min_revenue=self.min_revenue,
            max_revenue=self.max_revenue,
            is_hire=operator.not_(self.is_hire),
            is_senility=self.is_senility
        )

    @property
    def upper_sibling(self):
        if self.level >= MANAGEMENT_LEVEL.large:
            raise ValueError("No upper management level for this stratify.")
        return Stratify.objects.get(
            management_type=self.management_type,
            is_hire=self.is_hire,
            level=self.level + 1,
            is_senility=self.is_senility
        )

    @property
    def lower_sibling(self):
        if self.level <= MANAGEMENT_LEVEL.small:
            raise ValueError("No lower management level for this stratify.")
        return Stratify.objects.get(
            management_type=self.management_type,
            is_hire=self.is_hire,
            level=self.level - 1,
            is_senility=self.is_senility
        )

    @cached_property
    def origin_sample_count(self):
        return self.farmer_stats.filter(sample_group=SAMPLE_GROUP.origin).count()

    @cached_property
    def mix_sample_count(self):
        return self.farmer_stats.filter(sample_group=SAMPLE_GROUP.mix).count()

    @cached_property
    def origin_magnification_factor(self):
        return self.get_magnification_factor("origin_sample_count")

    @cached_property
    def mix_magnification_factor(self):
        return self.get_magnification_factor("mix_sample_count")

    def get_magnification_factor(self, sample_count_method="origin_sample_count"):
        # 各層母體數 / 各層樣本數
        # case a: 小/大型同規模有/無僱合併
        if (
            self.level != MANAGEMENT_LEVEL.middle
            and getattr(self.sibling, sample_count_method) == 0
            and getattr(self, sample_count_method) > 0
        ):
            return (self.population + self.sibling.population) / getattr(self, sample_count_method)
        # case b: 中型要考量更多情況
        elif self.level == MANAGEMENT_LEVEL.middle:
            population, sample_count = self.population, getattr(self, sample_count_method)
            # case b.1: 同規模有/無僱合併
            if getattr(self.sibling, sample_count_method) == 0:
                population += self.sibling.population
            # case b.2: 小型併入中型
            if getattr(self.lower_sibling, sample_count_method) == 0:
                population += self.lower_sibling.population
                # case b.2-1: 小型有/無僱皆為0
                if getattr(self.lower_sibling.sibling, sample_count_method) == 0:
                    population += self.lower_sibling.sibling.population
            # case b.3: 大型併入中型
            if getattr(self.upper_sibling, sample_count_method) == 0:
                population += self.upper_sibling.population
                # case b.3-1: 大型有/無僱皆為0
                if getattr(self.upper_sibling.sibling, sample_count_method) == 0:
                    population += self.upper_sibling.sibling.population
            return population / sample_count
        return self.population / getattr(self, sample_count_method)


class FarmerStat(Model):
    survey = OneToOneField(
        "surveys24.Survey",
        on_delete=CASCADE,
        related_name="farmer_stat",
        verbose_name=_("Survey"),
    )
    stratify = ForeignKey(
        "surveys24.Stratify",
        on_delete=CASCADE,
        related_name="farmer_stats",
        verbose_name=_("Stratify"),
    )
    is_senility = BooleanField(
        null=True, blank=True, verbose_name=_("Is Senility")
    )
    sample_group = PositiveIntegerField(
        null=True, blank=True, choices=SAMPLE_GROUP, verbose_name=_("Sample Group")
    )
    create_time = AutoCreatedField(_("Create Time"))
    update_time = AutoLastModifiedField(_("Update Time"))

    class Meta:
        verbose_name = _("Farmer Stat")
        verbose_name_plural = _("Farmer Stat")

    def __str__(self):
        return str(self.survey)

    @classmethod
    def get_is_senility(cls, survey: Survey) -> bool:
        # 高齡：戶內皆為超過65歲(出生年＜47年次)從農者自家農牧業工作一日以上）

        old_worker = young_worker = False
        for obj in survey.populations.filter(farmer_work_day__id__gt=1):
            if obj.birth_year < 47:
                old_worker = True
            else:
                young_worker = True

        if old_worker and not young_worker:
            return True

        return False

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
                origin_is_senility = survey.origin_class >= 101
                is_senility = cls.get_is_senility(survey)
                stratify = cls.get_stratify(survey, is_senility)
                stats.append(
                    cls(
                        survey=survey,
                        stratify=stratify,
                        is_senility=is_senility,
                        sample_group=(
                            SAMPLE_GROUP.origin if origin_is_senility == is_senility
                            else SAMPLE_GROUP.mix
                        )
                    )
                )
            except Stratify.DoesNotExist:
                print(f"Cannot find stratify for survey {survey}.")

        # Bulk operation
        cls.objects.all().delete()
        cls.objects.bulk_create(stats)

    @staticmethod
    def get_stratify(survey: Survey, is_senility: bool):
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
                is_senility=is_senility
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
                    is_senility=is_senility
                )
            else:
                raise ValueError(f"Survey {survey}'s annual income is missing.")


class ForeignLaborHire(Model):
    """
    (New table added in 24)
    Table 4.2
    """

    survey = ForeignKey(
        "surveys24.Survey",
        related_name="foreign_labor_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    month = ForeignKey(
        "surveys24.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    hire_type = PositiveIntegerField(
        choices=FOREIGN_LABOR_HIRE_TYPE, verbose_name=_("Hire Type")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ForeignLaborHire")
        verbose_name_plural = _("ForeignLaborHire")
        ordering = ("month",)

    def __str__(self):
        return str(self.survey)
