from django.contrib import admin
from date_range_filter import DateRangeFilter
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

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
    BuilderFile,
)


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


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "farmer_id",
        "farmer_name",
        "total_pages",
        "page",
        "readonly",
        "update_time",
    )
    list_filter = (
        "readonly",
        "page",
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
        """Django suit 的 DateFilter 需要引用的外部資源 """
        js = ['/admin/jsi18n/']


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
admin.site.register(ProductType)
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
admin.site.register(BuilderFile)
