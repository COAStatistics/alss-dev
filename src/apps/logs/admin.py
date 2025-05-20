from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.fields import Field

from date_range_filter import DateRangeFilter

from .models import ReviewLog


YEAR_APP_MAP = {}
APP_YEAR_MAP = {}
for year, app in zip(
    ("106", "107", "108", "110", "111", "112", "113"),
    ("surveys18", "surveys19", "surveys20", "surveys22", "surveys23", "surveys24", "surveys25"),
):
    YEAR_APP_MAP[year] = app
    APP_YEAR_MAP[app] = year


class ReviewLogResource(ModelResource):
    farmer_id = Field(column_name=_("Farmer Id"))
    year = Field(column_name="年份")
    user = Field(column_name=_("User"))
    initial_errors = Field(
        attribute="initial_errors", column_name=_("Initialed Error Count")
    )
    current_errors = Field(
        attribute="current_errors", column_name=_("Current Error Count")
    )
    exception_errors = Field(
        attribute="exception_errors", column_name=_("Exception Error Count")
    )
    update_time = Field(attribute="update_time", column_name=_("Updated"))

    class Meta:
        model = ReviewLog
        exclude = ("id", "content_type", "content_object", "object_id")

    def dehydrate_user(self, obj):
        return obj.user.full_name

    def dehydrate_farmer_id(self, obj):
        if obj.content_object:
            return obj.content_object.farmer_id
        return "此調查表已經被刪除"

    def dehydrate_year(self, obj):
        return APP_YEAR_MAP[obj.content_type.app_label]


class YearFilter(SimpleListFilter):
    title = "year"
    parameter_name = "y"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(y, y) for y in YEAR_APP_MAP.keys()]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() in YEAR_APP_MAP:
            return queryset.filter(content_type__app_label=YEAR_APP_MAP[self.value()])
        else:
            return queryset


class ReviewLogAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReviewLogResource
    list_display = (
        "id",
        "user",
        "year",
        "farmer_id",
        "initial_errors",
        "exception_errors",
        "current_errors",
        "update_time",
    )
    list_filter = (
        "user",
        YearFilter,
        "initial_errors",
        "exception_errors",
        "current_errors",
        ("update_time", DateRangeFilter),
    )
    search_fields = ("user__full_name",)

    def farmer_id(self, obj):
        if obj.content_object:
            return obj.content_object.farmer_id
        return "此調查表已經被刪除"

    farmer_id.short_description = "農戶編號"

    def year(self, obj):
        return APP_YEAR_MAP[obj.content_type.app_label]

    year.short_description = "年份"

    class Media:
        """Django suit 的 DateFilter 需要引用的外部資源"""

        js = ["/admin/jsi18n/"]


admin.site.register(ReviewLog, ReviewLogAdmin)
