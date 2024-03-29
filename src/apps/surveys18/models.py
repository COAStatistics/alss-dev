from django.conf import settings
from django.db.transaction import atomic
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Model,
    CASCADE,
    SET_NULL,
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
    Q,
    FileField,
    Count,
    Max,
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

NUMBER_WORKERS_CHOICES = Q(app_label="surveys18", model="longtermhire") | Q(
    app_label="surveys18", model="shorttermhire"
)


class BuilderFileType(Model):
    name = CharField(max_length=50, unique=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("BuilderFileType")
        verbose_name_plural = _("BuilderFileType")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class BuilderFile(Model):
    create_time = DateTimeField(auto_now_add=True, verbose_name=_("Create Time"))
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="surveys18_files",
        verbose_name=_("User"),
    )
    token = TextField(null=True, blank=True, verbose_name=_("Token String"))
    datafile = FileField(
        null=True,
        blank=True,
        upload_to="surveys18/builders/",
        verbose_name=_("DataFile"),
    )
    type = ForeignKey(
        "surveys18.BuilderFileType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("BuilderFileType"),
    )

    class Meta:
        verbose_name = _("BuilderFile")
        verbose_name_plural = _("BuilderFile")

    def __str__(self):
        return str(self.type)

    def __unicode__(self):
        return str(self.type)


class Survey(Model):
    """
    read_only: Keep original data(read_only=True). Modify data(read_only=False).
    """

    farmer_id = CharField(max_length=12, verbose_name=_("Farmer Id"))
    farmer_name = CharField(
        null=True, blank=True, max_length=10, verbose_name=_("Name")
    )
    total_pages = IntegerField(verbose_name=_("Total Pages"))
    page = IntegerField(verbose_name=_("Page"))
    origin_class = IntegerField(null=True, blank=True, verbose_name=_("Origin Class"))
    hire = BooleanField(default=False, verbose_name=_("Hire"))
    non_hire = BooleanField(default=False, verbose_name=_("Non Hire"))
    lacks = ManyToManyField(
        "surveys18.Lack", blank=True, related_name="surveys18", verbose_name=_("Lack")
    )
    management_types = ManyToManyField(
        "surveys18.ManagementType",
        blank=True,
        related_name="surveys",
        verbose_name=_("Management Types"),
    )
    note = TextField(null=True, blank=True, verbose_name=_("Note"))
    is_updated = BooleanField(default=False, verbose_name=_("Is Updated"))
    readonly = BooleanField(default=True, verbose_name=_("Read Only"))

    investigator = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="surveys18",
        verbose_name=_("Investigator"),
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

    review_logs = GenericRelation(ReviewLog, related_query_name="surveys18")

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Survey")

    def __str__(self):
        return self.farmer_id

    def __unicode__(self):
        return self.farmer_id


class ShortTermLack(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="short_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys18.Product",
        related_name="short_term_lacks",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Product"),
    )
    work_type = ForeignKey(
        "surveys18.WorkType",
        null=True,
        related_name="short_term_lacks",
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Work Type"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys18.Month",
        blank=True,
        related_name="short_term_lacks",
        verbose_name=_("Months"),
    )
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

    def __unicode__(self):
        return str(self.survey)


class LongTermLack(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="long_term_lacks",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    work_type = ForeignKey(
        "surveys18.WorkType",
        null=True,
        related_name="long_term_lacks",
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Work Type"),
    )
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    months = ManyToManyField(
        "surveys18.Month",
        blank=True,
        related_name="long_term_lacks",
        verbose_name=_("Months"),
    )
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

    def __unicode__(self):
        return str(self.survey)


class NoSalaryHire(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="no_salary_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    month = ForeignKey(
        "surveys18.Month",
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

    def __unicode__(self):
        return str(self.survey)


class NumberWorkers(Model):
    content_type = ForeignKey(
        ContentType, on_delete=CASCADE, limit_choices_to=NUMBER_WORKERS_CHOICES
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    age_scope = ForeignKey(
        "surveys18.AgeScope",
        on_delete=CASCADE,
        related_name="number_workers",
        null=True,
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

    def __unicode__(self):
        return str(self.content_object)


class AgeScope(Model):
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

    def __unicode__(self):
        return str(self.name)


class WorkType(Model):
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

    def __unicode__(self):
        return str(self.name)


class ShortTermHire(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="short_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    month = ForeignKey(
        "surveys18.Month",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Month"),
    )
    work_types = ManyToManyField(
        "surveys18.WorkType",
        blank=True,
        related_name="short_term_hires",
        verbose_name=_("Work Types"),
    )
    number_workers = GenericRelation(
        NumberWorkers, related_query_name="short_term_hires"
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

    def __unicode__(self):
        return str(self.survey)


class LongTermHire(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="long_term_hires",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    avg_work_day = FloatField(null=True, blank=True, verbose_name=_("Average Work Day"))
    work_type = ForeignKey(
        "surveys18.WorkType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="long_term_hires",
        verbose_name=_("Work Type"),
    )
    months = ManyToManyField(
        "surveys18.Month",
        blank=True,
        related_name="long_term_hires",
        verbose_name=_("Months"),
    )
    number_workers = GenericRelation(
        NumberWorkers, related_query_name="long_term_hires"
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

    def __unicode__(self):
        return str(self.survey)


class Subsidy(Model):
    survey = OneToOneField(
        "surveys18.Survey",
        related_name="subsidy",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    has_subsidy = BooleanField(default=False, verbose_name=_("Has Subsidy"))
    none_subsidy = BooleanField(default=False, verbose_name=_("None Subsidy"))
    count = IntegerField(null=True, blank=True, verbose_name=_("Number Of People"))
    month_delta = IntegerField(null=True, blank=True, verbose_name=_("Month Delta"))
    day_delta = IntegerField(null=True, blank=True, verbose_name=_("Day Delta"))
    hour_delta = IntegerField(null=True, blank=True, verbose_name=_("Hour Delta"))
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

    def __unicode__(self):
        return str(self.survey)


class Refuse(Model):
    subsidy = ForeignKey(
        "surveys18.Subsidy",
        related_name="refuses",
        on_delete=CASCADE,
        verbose_name=_("Subsidy"),
    )
    reason = ForeignKey(
        "surveys18.RefuseReason",
        related_name="refuse",
        null=True,
        blank=True,
        on_delete=CASCADE,
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

    def __unicode__(self):
        return str(self.reason)


class RefuseReason(Model):
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

    def __unicode__(self):
        return str(self.name)


class Population(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="populations",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    relationship = ForeignKey(
        "surveys18.Relationship",
        related_name="relationship",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Relationship"),
    )
    gender = ForeignKey(
        "surveys18.Gender",
        related_name="relationship",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Gender"),
    )
    birth_year = IntegerField(null=True, blank=True, verbose_name=_("Birth Year"))
    education_level = ForeignKey(
        "surveys18.EducationLevel",
        related_name="education_level",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Education Level"),
    )
    farmer_work_day = ForeignKey(
        "surveys18.FarmerWorkDay",
        related_name="farmer_work_day",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Farmer Work Day"),
    )
    life_style = ForeignKey(
        "surveys18.LifeStyle",
        related_name="life_style",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Life Style"),
    )
    other_farm_work = ForeignKey(
        "surveys18.OtherFarmWork",
        related_name="other_farm_work",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Other Farm Work"),
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

    def __unicode__(self):
        return str(self.survey)


class FarmerWorkDay(Model):
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
        verbose_name = _("FarmerWorkDay")
        verbose_name_plural = _("FarmerWorkDay")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class OtherFarmWork(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("OtherFarmWork")
        verbose_name_plural = _("OtherFarmWork")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Relationship(Model):
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

    def __unicode__(self):
        return str(self.name)


class EducationLevel(Model):
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

    def __unicode__(self):
        return str(self.name)


class LifeStyle(Model):
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

    def __unicode__(self):
        return str(self.name)


class Gender(Model):
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

    def __unicode__(self):
        return str(self.name)


class PopulationAge(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="population_ages",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    gender = ForeignKey(
        "surveys18.Gender",
        verbose_name=_("Gender"),
        on_delete=CASCADE,
        null=True,
        blank=True,
    )
    age_scope = ForeignKey(
        "surveys18.AgeScope",
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

    def __unicode__(self):
        return str(self.survey)


class CropMarketing(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="crop_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys18.Product",
        related_name="products",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Product Code"),
    )
    loss = ForeignKey(
        "surveys18.Loss",
        related_name="crop_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys18.Unit",
        related_name="crop_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    land_number = IntegerField(null=True, blank=True, verbose_name=_("Land Number"))
    land_area = IntegerField(null=True, blank=True, verbose_name=_("Land Area"))
    plant_times = IntegerField(null=True, blank=True, verbose_name=_("Plant Times"))
    total_yield = IntegerField(null=True, blank=True, verbose_name=_("Total Yield"))
    unit_price = IntegerField(null=True, blank=True, verbose_name=_("Unit Price"))
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

    def __unicode__(self):
        return str(self.survey)


class LivestockMarketing(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="livestock_marketings",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    product = ForeignKey(
        "surveys18.Product",
        related_name="livestock_marketing_product",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Product"),
    )
    loss = ForeignKey(
        "surveys18.Loss",
        related_name="livestock_marketing_loss",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Loss"),
    )
    unit = ForeignKey(
        "surveys18.Unit",
        related_name="livestock_marketing_unit",
        on_delete=CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Unit"),
    )
    contract = ForeignKey(
        "surveys18.Contract",
        related_name="contract",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Contract"),
    )
    raising_number = IntegerField(
        null=True, blank=True, verbose_name=_("Raising Number")
    )
    total_yield = IntegerField(null=True, blank=True, verbose_name=_("Total Yield"))
    unit_price = IntegerField(null=True, blank=True, verbose_name=_("Unit Price"))
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

    def __unicode__(self):
        return str(self.survey)


class Loss(Model):
    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    type = ForeignKey(
        "surveys18.ProductType",
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

    def __unicode__(self):
        return str(self.name)


class Unit(Model):
    code = IntegerField(verbose_name=_("Code"))
    name = CharField(max_length=10, null=True, blank=True, verbose_name=_("Name"))
    type = ForeignKey(
        "surveys18.ProductType",
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

    def __unicode__(self):
        return str(self.name)


class ProductType(Model):
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Type")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Product(Model):
    name = CharField(max_length=50, null=True, blank=True, verbose_name=_("Name"))
    code = CharField(max_length=50, verbose_name=_("Code"))
    type = ForeignKey(
        "surveys18.ProductType",
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
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Contract(Model):
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
        verbose_name = _("LivestockUnit")
        verbose_name_plural = _("LivestockUnit")

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class ManagementType(Model):
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

    def __unicode__(self):
        return str(self.name)


class Business(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="businesses",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    farm_related_business = ForeignKey(
        "surveys18.FarmRelatedBusiness",
        null=True,
        blank=True,
        related_name="business",
        on_delete=CASCADE,
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


class FarmRelatedBusiness(Model):
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

    def __unicode__(self):
        return str(self.name)


class LandStatus(Model):
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

    def __unicode__(self):
        return self.name


class LandType(Model):
    name = CharField(max_length=20, null=True, blank=True, verbose_name=_("Name"))
    statuses = ManyToManyField(
        "surveys18.LandStatus",
        blank=True,
        related_name="land_type",
        verbose_name=_("Land Statuses"),
    )
    unit = ForeignKey(
        "surveys18.Unit",
        related_name="land_type",
        on_delete=CASCADE,
        null=True,
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

    def __unicode__(self):
        return self.name


class LandArea(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="land_areas",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    type = ForeignKey(
        "surveys18.LandType",
        related_name="land_areas",
        null=True,
        on_delete=CASCADE,
        blank=True,
        verbose_name=_("Type"),
    )
    status = ForeignKey(
        "surveys18.LandStatus",
        related_name="land_areas",
        null=True,
        on_delete=CASCADE,
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

    def __unicode__(self):
        return str(self.survey)


class Phone(Model):
    survey = ForeignKey(
        "surveys18.Survey",
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

    def __unicode__(self):
        return str(self.survey)


class Lack(Model):
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

    def __unicode__(self):
        return str(self.name)


class AddressMatch(Model):
    survey = OneToOneField(
        "surveys18.Survey",
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

    def __unicode__(self):
        return str(self.survey)


class IncomeRange(Model):
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
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class MarketType(Model):
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

    def __unicode__(self):
        return str(self.name)


class AnnualIncome(Model):
    survey = ForeignKey(
        "surveys18.Survey",
        related_name="annual_incomes",
        on_delete=CASCADE,
        verbose_name=_("Survey"),
    )
    market_type = ForeignKey(
        "surveys18.MarketType",
        null=True,
        blank=True,
        on_delete=CASCADE,
        verbose_name=_("Market Type"),
    )
    income_range = ForeignKey(
        "surveys18.IncomeRange",
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

    def __unicode__(self):
        return str(self.survey)


class Month(Model):
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

    def __unicode__(self):
        return str(self.name)


class Stratify(Model):
    """
    field=公畝;revenue=萬元
    """

    management_type = ForeignKey(
        "surveys18.ManagementType",
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
    """
    106年牽涉主力農家及手動無效戶調整，無法透過固定邏輯自動計算，出現在此表的農戶才是實質意義的有效戶
    另外由於原始調查表的地址可能為空值（與調查名冊相同的情況），因此將農戶所在地區一併紀錄在此表（僅有效戶需要區域資訊）
    請透過後台將靜態結果匯入
    """

    survey = OneToOneField(
        "surveys18.Survey",
        on_delete=CASCADE,
        related_name="farmer_stat",
        verbose_name=_("Survey"),
    )
    stratify = ForeignKey(
        "surveys18.Stratify",
        on_delete=CASCADE,
        related_name="farmer_stats",
        verbose_name=_("Stratify"),
    )
    region = PositiveIntegerField(choices=REGION_CHOICES, verbose_name=_("Region"))
    create_time = AutoCreatedField(_("Create Time"))
    update_time = AutoLastModifiedField(_("Update Time"))

    class Meta:
        verbose_name = _("Farmer Stat")
        verbose_name_plural = _("Farmer Stat")

    def __str__(self):
        return str(self.survey)
