from django.contrib import admin
from rangefilter.filter import DateRangeFilter
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from .models import (
    BuilderFile,
    BuilderFileType,
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    Lack,
    Phone,
    LandArea,
    LandType,
    LandStatus,
    FarmRelatedBusiness,
    ManagementType,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    LivestockMarketing,
    Facility,
    PopulationAge,
    Population,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    OtherFarmWork,
    Subsidy,
    RefuseReason,
    AgeScope,
    LongTermHire,
    ShortTermHire,
    WorkType,
    NumberWorkers,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
    Gender,
    ProductType,
    Business,
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
        "is_updated",
        "update_time",
    )
    list_filter = (
        "is_updated",
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


admin.site.register(Survey, SurveyAdmin)
admin.site.register(BuilderFile)
admin.site.register(BuilderFileType)
admin.site.register(MarketType)
admin.site.register(IncomeRange)
admin.site.register(AnnualIncome)
admin.site.register(AddressMatch)
admin.site.register(Lack)
admin.site.register(Phone)
admin.site.register(LandArea)
admin.site.register(LandType)
admin.site.register(LandStatus)
admin.site.register(Business)
admin.site.register(FarmRelatedBusiness)
admin.site.register(ManagementType)
admin.site.register(Loss)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Contract)
admin.site.register(CropMarketing)
admin.site.register(LivestockMarketing)
admin.site.register(Facility)
admin.site.register(PopulationAge)
admin.site.register(Population)
admin.site.register(EducationLevel)
admin.site.register(FarmerWorkDay)
admin.site.register(LifeStyle)
admin.site.register(OtherFarmWork)
admin.site.register(Subsidy)
admin.site.register(RefuseReason)
admin.site.register(AgeScope)
admin.site.register(WorkType)
admin.site.register(LongTermHire)
admin.site.register(ShortTermHire)
admin.site.register(NumberWorkers)
admin.site.register(NoSalaryHire)
admin.site.register(ShortTermLack)
admin.site.register(LongTermLack)
admin.site.register(Gender)
admin.site.register(ProductType)
