from django.contrib import admin

from django.contrib.admin import SimpleListFilter

from date_range_filter import DateRangeFilter

from .models import ReviewLog


class YearFilter(SimpleListFilter):
    title = 'year'
    parameter_name = 'y'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('106', '106'), ('107', '107')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == '106':
            return queryset.filter(content_type__app_label='surveys18')
        if self.value() == '107':
            return queryset.filter(content_type__app_label='surveys19')
        else:
            return queryset


class ReviewLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "year",
        "farmer_id",
        "initial_errors",
        "current_errors",
        "update_datetime",
    )
    list_filter = (
        "user",
        YearFilter,
        "initial_errors",
        "current_errors",
        ("update_datetime", DateRangeFilter),
    )
    search_fields = ("user__full_name",)

    def farmer_id(self, obj):
        return obj.content_object.farmer_id
    farmer_id.short_description = '農戶編號'

    def year(self, obj):
        if obj.content_type.app_label == 'surveys18':
            return '106'
        if obj.content_type.app_label == 'surveys19':
            return '107'
    year.short_description = '年份'

    class Media:
        """Django suit 的 DateFilter 需要引用的外部資源 """
        js = ['/admin/jsi18n/']


admin.site.register(ReviewLog, ReviewLogAdmin)
