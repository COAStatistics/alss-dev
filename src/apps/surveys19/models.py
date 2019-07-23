from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
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
from apps.logs.models import ReviewLog


YES_NO_CHOICES = ((0, "No"), (1, "Yes"))

NUMBER_WORKERS_CHOICES = Q(app_label="surveys19", model="longtermhire") | Q(
    app_label="surveys19", model="shorttermhire"
)


class Survey(Model):
    """
    read_only: Keep original data(read_only=True). Modify data(read_only=False).
    new field second and non_second table 1.4
    """

    farmer_id = CharField(max_length=12, verbose_name=_("Farmer Id"), db_index=True)
    farmer_name = CharField(
        null=True, blank=True, max_length=10, verbose_name=_("Name")
    )
    total_pages = IntegerField(verbose_name=_("Total Pages"))
    page = IntegerField(verbose_name=_("Page"))
    origin_class = IntegerField(null=True, blank=True, verbose_name=_("Origin Class"))
    second = BooleanField(default=False, verbose_name=_("Second"))
    non_second = BooleanField(default=False, verbose_name=_("Non Second"))
    hire = BooleanField(default=False, verbose_name=_("Hire"))
    non_hire = BooleanField(default=False, verbose_name=_("Non Hire"))
    lacks = ManyToManyField(
        "surveys19.Lack", blank=True, related_name="surveys", verbose_name=_("Lack")
    )
    management_types = ManyToManyField(
        "surveys19.ManagementType",
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

    review_logs = GenericRelation(ReviewLog, related_query_name="surveys19")

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
        "surveys19.Survey",
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
        "surveys19.Survey",
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
        "surveys19.Survey",
        related_name="farm_location",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    city = CharField(max_length=20, null=True, blank=True, verbose_name=_("City"))
    town = CharField(max_length=20, null=True, blank=True, verbose_name=_("Town"))
    code = ForeignKey(
        "surveys19.CityTownCode",
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
        "surveys19.LandStatus",
        blank=True,
        related_name="land_type",
        verbose_name=_("Land Statuses"),
    )
    unit = ForeignKey(
        "surveys19.Unit",
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
        "surveys19.Survey",
        related_name="land_areas",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    type = ForeignKey(
        "surveys19.LandType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="land_areas",
        verbose_name=_("Type"),
    )
    status = ForeignKey(
        "surveys19.LandStatus",
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
        "surveys19.Survey",
        related_name="businesses",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    farm_related_business = ForeignKey(
        "surveys19.FarmRelatedBusiness",
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
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
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
        "surveys19.Survey",
        related_name="crop_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys19.Product",
        related_name="products",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Product Code"),
    )
    loss = ForeignKey(
        "surveys19.Loss",
        related_name="crop_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys19.Unit",
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
        "surveys19.Survey",
        related_name="livestock_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys19.Product",
        related_name="livestock_marketing_product",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Product"),
    )
    loss = ForeignKey(
        "surveys19.Loss",
        related_name="livestock_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys19.Unit",
        related_name="livestock_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    contract = ForeignKey(
        "surveys19.Contract",
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


class ProductType(Model):
    """
    Table 1.5, 1.6
    Has yaml
    """

    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ProductType")
        verbose_name_plural = _("ProductType")

    def __str__(self):
        return str(self.name)


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
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE, verbose_name=_('Parent Product'))
    type = ForeignKey(
        "surveys19.ProductType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Product Type"),
    )
    management_type = ForeignKey(
        "surveys19.ManagementType",
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
        ordering = ('id', 'code',)

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
    type = ForeignKey(
        "surveys19.ProductType",
        null=True,
        blank=True,
        on_delete=CASCADE,
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
    type = ForeignKey(
        "surveys19.ProductType",
        null=True,
        blank=True,
        on_delete=CASCADE,
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
        "surveys19.Survey",
        related_name="annual_incomes",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    market_type = ForeignKey(
        "surveys19.MarketType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Market Type"),
    )
    income_range = ForeignKey(
        "surveys19.IncomeRange",
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
        "surveys19.Survey",
        related_name="population_ages",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    gender = ForeignKey(
        "surveys19.Gender",
        verbose_name=_("Gender"),
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    age_scope = ForeignKey(
        "surveys19.AgeScope",
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
        "surveys19.Survey",
        related_name="populations",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    relationship = ForeignKey(
        "surveys19.Relationship",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Relationship"),
    )
    gender = ForeignKey(
        "surveys19.Gender",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="relationship",
        verbose_name=_("Gender"),
    )
    birth_year = IntegerField(null=True, blank=True, verbose_name=_("Birth Year"))
    education_level = ForeignKey(
        "surveys19.EducationLevel",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="education_level",
        verbose_name=_("Education Level"),
    )
    farmer_work_day = ForeignKey(
        "surveys19.FarmerWorkDay",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="farmer_work_day",
        verbose_name=_("Farmer Work Day"),
    )
    life_style = ForeignKey(
        "surveys19.LifeStyle",
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
        "surveys19.Survey",
        related_name="long_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    work_type = ForeignKey(
        "surveys19.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_hires",
        verbose_name=_("Work Type"),
    )
    months = ManyToManyField(
        "surveys19.Month",
        blank=True,
        related_name="long_term_hires",
        verbose_name=_("Months"),
    )
    number_workers = GenericRelation(
        "surveys19.NumberWorkers", related_query_name="long_term_hires"
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
        "surveys19.Survey",
        related_name="short_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    month = ForeignKey(
        "surveys19.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    work_types = ManyToManyField(
        "surveys19.WorkType",
        blank=True,
        related_name="short_term_hires",
        verbose_name=_("Work Types"),
    )
    number_workers = GenericRelation(
        "surveys19.NumberWorkers", related_query_name="short_term_hires"
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
        "surveys19.Survey",
        related_name="no_salary_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    month = ForeignKey(
        "surveys19.Month",
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
        related_name="number_workers",
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    age_scope = ForeignKey(
        "surveys19.AgeScope",
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
        "surveys19.Survey",
        related_name="long_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    work_type = ForeignKey(
        "surveys19.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_lacks",
        verbose_name=_("Work Type"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys19.Month",
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
        "surveys19.Survey",
        related_name="short_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys19.Product",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="short_term_lacks",
        verbose_name=_("Product"),
    )
    work_type = ForeignKey(
        "surveys19.WorkType",
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
        "surveys19.Month",
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
    Table 3.3.1
    """

    survey = OneToOneField(
        "surveys19.Survey",
        related_name="subsidy",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    has_subsidy = BooleanField(default=False, verbose_name=_("Has Subsidy"))
    none_subsidy = BooleanField(default=False, verbose_name=_("None Subsidy"))
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    month_delta = IntegerField(null=True, blank=True, verbose_name=_("Month Delta"))
    day_delta = IntegerField(null=True, blank=True, verbose_name=_("Day Delta"))
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
        "surveys19.Subsidy",
        related_name="refuses",
        on_delete=CASCADE,
        verbose_name=_("Subsidy"),
    )
    reason = ForeignKey(
        "surveys19.RefuseReason",
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
        related_name="surveys19_files",
        verbose_name=_("User"),
    )
    token = TextField(null=True, blank=True, verbose_name=_("Token String"))
    datafile = FileField(
        null=True,
        blank=True,
        upload_to="surveys19/builders/",
        verbose_name=_("DataFile"),
    )
    delete_exist = BooleanField(default=False)

    class Meta:
        verbose_name = _("BuilderFile")
        verbose_name_plural = _("BuilderFile")

    def __str__(self):
        return str(self.user)
