from django.contrib import admin
from date_range_filter import DateRangeFilter
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.fields import Field


from .models import (
    Survey,
    Phone,
    AddressMatch,
    FarmLocation,
    LandStatus,
    LandType,
    LandArea,
    Business,
    FarmRelatedBusiness,
    ManagementType,
    CropMarketing,
    LivestockMarketing,
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
    BuilderFile,
    CityTownCode,
    Stratify,
    FarmerStat,
    MANAGEMENT_LEVEL,
)


def display_note(obj, sample_count_method="origin_sample_count"):
    if getattr(obj, sample_count_method) == 0:
        if getattr(obj.sibling, sample_count_method) > 0:
            return f"併入{obj.sibling.code}層"
        elif obj.level == MANAGEMENT_LEVEL.middle:
            if getattr(obj.lower_sibling, sample_count_method) == 0:
                # 中下層都沒有，併入大層
                return f"併入{obj.upper_sibling.code}層"
            return f"特殊情況須額外處理"
        elif obj.level == MANAGEMENT_LEVEL.small:
            if getattr(obj.upper_sibling, sample_count_method) == 0:
                if getattr(obj.upper_sibling.sibling, sample_count_method) > 0:
                    # 上層 sibling 有
                    return f"併入{obj.upper_sibling.sibling.code}層"
                # 上層 sibling 也沒有，併入大層
                return f"併入{obj.upper_sibling.upper_sibling.code}層"
            return f"併入{obj.upper_sibling.code}層"
        elif obj.level == MANAGEMENT_LEVEL.large:
            if getattr(obj.lower_sibling, sample_count_method) == 0:
                # 連下層都沒有就併入下層的 sibling
                return f"併入{obj.lower_sibling.sibling.code}層"
            return f"併入{obj.lower_sibling.code}層"
        else:
            return f"特殊情況須額外處理"
    return ""


class StratifyResource(ModelResource):
    agg_management_type_display = Field(
        attribute="agg_management_type_display", column_name=_("Management Type")
    )
    code = Field(attribute="code", column_name=_("Code"))
    population = Field(attribute="population", column_name=_("Population(Statistic)"))
    origin_sample_count = Field(column_name=_("Origin Sample Count"))
    origin_magnification_factor = Field(column_name=_("Origin Magnification Factor"))
    mix_sample_count = Field(column_name=_("Mix Sample Count"))
    mix_magnification_factor = Field(column_name=_("Mix Magnification Factor"))

    class Meta:
        model = Stratify
        fields = (
            "agg_management_type_display",
            "code",
            "population",
            "origin_sample_count",
            "origin_magnification_factor",
            "origin_note",
            "mix_sample_count",
            "mix_magnification_factor",
            "mix_note",
        )

    def dehydrate_origin_sample_count(self, obj):
        return obj.origin_sample_count

    def dehydrate_mix_sample_count(self, obj):
        return obj.mix_sample_count

    def dehydrate_origin_magnification_factor(self, obj):
        try:
            return obj.origin_magnification_factor
        except ZeroDivisionError:
            return "-"

    def dehydrate_mix_magnification_factor(self, obj):
        try:
            return obj.mix_magnification_factor
        except ZeroDivisionError:
            return "-"

    def dehydrate_origin_note(self, obj):
        return display_note(obj, sample_count_method="origin_sample_count")

    def dehydrate_mix_note(self, obj):
        return display_note(obj, sample_count_method="mix_sample_count")


class FarmerStatResource(ModelResource):
    survey = Field(attribute="survey", column_name=_("Farmer ID"))
    stratify = Field(attribute="stratify", column_name=_("Stratify"))

    class Meta:
        model = FarmerStat
        fields = ("farmer_id", "stratify")
        ordering = ("stratify__code",)


class ProductFilter(SimpleListFilter):
    title = "Product"
    parameter_name = "product"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        crops = CropMarketing.objects.values_list("product__id", flat=True).distinct()
        livestocks = LivestockMarketing.objects.values_list(
            "product__id", flat=True
        ).distinct()
        for product in Product.objects.filter(
            Q(id__in=crops) | Q(id__in=livestocks)
        ).all():
            list_tuple.append((product.id, product.name))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            crop_related_surveys = CropMarketing.objects.filter(
                product__id=self.value()
            ).values_list("survey__id", flat=True)
            livestock_related_surveys = LivestockMarketing.objects.filter(
                product__id=self.value()
            ).values_list("survey__id", flat=True)
            return queryset.filter(
                Q(id__in=crop_related_surveys) | Q(id__in=livestock_related_surveys)
            )
        else:
            return queryset


class SurveyAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "farmer_id",
        "farmer_name",
        "total_pages",
        "page",
        "readonly",
        "note",
        "invalid_reason",
        "update_time",
    )
    list_filter = (
        "readonly",
        "page",
        "is_invalid",
        ProductFilter,
        ("update_time", DateRangeFilter),
    )
    search_fields = ("farmer_id", "farmer_name")

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(SurveyAdmin, self).get_search_results(
            request, queryset, search_term
        )
        if search_term:
            try:
                int(search_term)
                queryset = self.model.objects.filter(
                    Q(farmer_id=search_term)
                    | Q(farmer_name=search_term)
                    | Q(id=search_term)
                )
            except ValueError:
                queryset = self.model.objects.filter(farmer_name=search_term)

        return queryset, use_distinct

    class Media:
        """Django suit 的 DateFilter 需要引用的外部資源"""

        js = ["/admin/jsi18n/"]


class StratifyAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StratifyResource
    list_display = (
        "agg_management_type_display",
        "is_hire",
        "code",
        "population",
        "level",
        "origin_sample_count",
        "origin_magnification_factor",
        "origin_note",
        "mix_sample_count",
        "mix_magnification_factor",
        "mix_note",
    )
    readonly_fields = ("origin_sample_count", "origin_magnification_factor", "origin_note")
    ordering = ("code",)

    def origin_sample_count(self, obj):
        return obj.origin_sample_count

    def mix_sample_count(self, obj):
        return obj.mix_sample_count

    def origin_magnification_factor(self, obj):
        try:
            return obj.origin_magnification_factor
        except ZeroDivisionError:
            return "-"

    def mix_magnification_factor(self, obj):
        try:
            return obj.mix_magnification_factor
        except ZeroDivisionError:
            return "-"

    def origin_note(self, obj):
        return display_note(obj, sample_count_method="origin_sample_count")

    def mix_note(self, obj):
        return display_note(obj, sample_count_method="mix_sample_count")

    origin_sample_count.short_description = _("Origin Sample Count")
    mix_sample_count.short_description = _("Mix Sample Count")
    origin_magnification_factor.short_description = _("Origin Magnification Factor")
    mix_magnification_factor.short_description = _("Mix Magnification Factor")
    origin_note.short_description = _("Origin Note")
    mix_note.short_description = _("Mix Note")


class FarmerStatAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = FarmerStatResource
    list_display = (
        "survey",
        "stratify",
    )
    search_fields = ("survey__farmer_id",)
    list_filter = ("stratify",)
    ordering = ("stratify__code",)


class BuilderFileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "short_token",
        "create_time",
    )
    search_fields = ("token",)

    def short_token(self, obj):
        return (obj.token[:100] + "...") if len(obj.token) > 100 else obj.token

    short_token.short_description = "Token"


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Phone)
admin.site.register(AddressMatch)
admin.site.register(FarmLocation)
admin.site.register(LandStatus)
admin.site.register(LandType)
admin.site.register(LandArea)
admin.site.register(Business)
admin.site.register(FarmRelatedBusiness)
admin.site.register(ManagementType)
admin.site.register(CropMarketing)
admin.site.register(LivestockMarketing)
admin.site.register(Product)
admin.site.register(Unit)
admin.site.register(Loss)
admin.site.register(Contract)
admin.site.register(AnnualIncome)
admin.site.register(MarketType)
admin.site.register(IncomeRange)
admin.site.register(AgeScope)
admin.site.register(PopulationAge)
admin.site.register(Population)
admin.site.register(Relationship)
admin.site.register(Gender)
admin.site.register(EducationLevel)
admin.site.register(FarmerWorkDay)
admin.site.register(LifeStyle)
admin.site.register(LongTermHire)
admin.site.register(ShortTermHire)
admin.site.register(NoSalaryHire)
admin.site.register(NumberWorkers)
admin.site.register(Lack)
admin.site.register(LongTermLack)
admin.site.register(ShortTermLack)
admin.site.register(WorkType)
admin.site.register(Subsidy)
admin.site.register(Refuse)
admin.site.register(RefuseReason)
admin.site.register(Month)
admin.site.register(BuilderFile, BuilderFileAdmin)
admin.site.register(CityTownCode)
admin.site.register(FarmerStat, FarmerStatAdmin)
admin.site.register(Stratify, StratifyAdmin)
