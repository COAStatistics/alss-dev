import os
import pandas
from string import ascii_lowercase
from openpyxl import load_workbook
from django.db.models import (
    Sum,
    Count,
    F,
    Case,
    When,
    Value,
    CharField,
    OuterRef,
    Subquery,
    IntegerField,
)
from django.db.models.functions import Concat, Coalesce, Cast
from django.contrib.postgres.aggregates import StringAgg
from django.conf import settings

from apps.surveys24.models import (
    Survey,
    LandArea,
    ManagementType,
    Lack,
    Refuse,
    Apply,
    ApplyMethod,
    RefuseReason,
    AnnualIncome,
    FarmRelatedBusiness,
    FarmerStat,
)


def column_generator(column_count):
    # Iterate over the column count
    for i in range(column_count):
        # For the first 26 columns, yield single letters
        if i < 26:
            yield ascii_lowercase[i]
        else:
            # For columns beyond 26, yield combinations of letters
            quotient, remainder = divmod(i, 26)
            yield ascii_lowercase[quotient - 1] + ascii_lowercase[remainder]


class RawDataExporter112:
    def __init__(self):
        template = os.path.join(
            settings.BASE_DIR, "config/export/templates/raw_data_112.xlsx"
        )
        self.wb = load_workbook(filename=template)
        invalid_farmers = (
            Survey.objects.filter(note__icontains="無效戶")
            .values_list("farmer_id", flat=True)
            .distinct()
        )
        self.survey_qs = Survey.objects.filter(readonly=False, is_invalid=False).exclude(
            farmer_id__in=invalid_farmers
        )

    def write_rows_by_queryset(self, sheet_name, column_counts, queryset):
        sheet = self.wb[sheet_name]
        for i, item in enumerate(queryset):
            row = i + 2
            for column in column_generator(column_counts):
                sheet[f"{column}{row}"] = item.get(f"field_{column}")

    def write_rows_by_dataframe(self, sheet_name, column_counts, dataframe):
        sheet = self.wb[sheet_name]
        for i, item in dataframe.iterrows():
            row = i + 2
            for column in column_generator(column_counts):
                sheet[f"{column}{row}"] = item.get(f"field_{column}")

    def process_sheet1(self):
        management_types = ManagementType.objects.filter(
            surveys__page=1, surveys__readonly=False, surveys=OuterRef("pk")
        )
        annual_incomes = AnnualIncome.objects.filter(
            survey__page=1, survey__readonly=False, survey=OuterRef("pk")
        )
        lacks = Lack.objects.filter(
            surveys__page=1, surveys__readonly=False, surveys=OuterRef("pk")
        )
        land_areas = LandArea.objects.filter(
            survey__page=1, survey__readonly=False, survey=OuterRef("pk")
        )

        qs1 = (
            self.survey_qs.filter(page=1)
            .prefetch_related(
                "land_areas",
                "farm_location__code",
                "population_ages",
            )
            .values("farmer_id")
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("farm_location__code__code"),
                field_c=Concat(
                    "farm_location__code__city",
                    "farm_location__code__town",
                    output_field=CharField(),
                ),
                field_d=Coalesce(
                    Subquery(land_areas.filter(type=1, status=1).values("value")), 0
                ),
                field_e=Coalesce(
                    Subquery(land_areas.filter(type=1, status=2).values("value")), 0
                ),
                field_f=Coalesce(
                    Subquery(land_areas.filter(type=1, status=3).values("value")), 0
                ),
                field_g=Coalesce(
                    Subquery(land_areas.filter(type=2, status=1).values("value")), 0
                ),
                field_h=Coalesce(
                    Subquery(land_areas.filter(type=2, status=2).values("value")), 0
                ),
                field_i=Subquery(management_types.values("code")[:1]),
                field_j=Coalesce(
                    Subquery(
                        annual_incomes.filter(market_type=1).values("income_range")
                    ),
                    0,
                ),
                field_k=Coalesce(
                    Subquery(
                        annual_incomes.filter(market_type=2).values("income_range")
                    ),
                    0,
                ),
                field_l=Coalesce(
                    Subquery(
                        annual_incomes.filter(market_type=3).values("income_range")
                    ),
                    0,
                ),
                field_m=Coalesce(
                    Subquery(
                        annual_incomes.filter(market_type=4).values("income_range")
                    ),
                    0,
                ),
                field_n=Coalesce(
                    Subquery(
                        annual_incomes.filter(market_type=5).values("income_range")
                    ),
                    0,
                ),
                field_o=Case(
                    When(
                        main_income_source=True,
                        non_main_income_source=False,
                        then=Value(1),
                    ),
                    When(
                        main_income_source=False,
                        non_main_income_source=True,
                        then=Value(2),
                    ),
                    default=Value(-1),
                    output_field=IntegerField(),
                ),
                field_p=Sum(
                    Case(
                        When(
                            population_ages__gender=1,
                            population_ages__age_scope=4,
                            then="population_ages__count",
                        ),
                        default=Value(0),
                    )
                ),
                field_q=Sum(
                    Case(
                        When(
                            population_ages__gender=2,
                            population_ages__age_scope=4,
                            then="population_ages__count",
                        ),
                        default=Value(0),
                    )
                ),
                field_r=Sum(
                    Case(
                        When(
                            population_ages__gender=1,
                            population_ages__age_scope=5,
                            then="population_ages__count",
                        ),
                        default=Value(0),
                    )
                ),
                field_s=Sum(
                    Case(
                        When(
                            population_ages__gender=2,
                            population_ages__age_scope=5,
                            then="population_ages__count",
                        ),
                        default=Value(0),
                    )
                ),
                field_t=Case(
                    When(hire=True, non_hire=False, then=Value(1)),
                    When(hire=False, non_hire=True, then=Value(2)),
                    default=Value(-1),
                    output_field=IntegerField(),
                ),
                field_u=Coalesce(Subquery(lacks.values("pk")), -1),
            )
        )

        df1 = pandas.DataFrame(qs1).set_index("field_a")
        df2 = pandas.DataFrame(
            0,
            index=df1.index,
            columns=[
                f"field_{i}" for i in ["v", "w", "x", "y", "z", "aa", "ab", "ac", "ad"]
            ],
        )

        non_heard_refuses = Refuse.objects.filter(
            subsidy__survey__page=1, subsidy__survey__readonly=False, reason__id=0
        ).annotate(method_pk=F("method__id"), farmer_id=F("subsidy__survey__farmer_id"))
        applies = Apply.objects.filter(
            subsidy__survey__page=1,
            subsidy__survey__readonly=False,
        ).annotate(
            method_pk=F("method__id"),
            farmer_id=F("subsidy__survey__farmer_id"),
            result_pk=F("result__id"),
        )

        for refuse in non_heard_refuses:
            if refuse.farmer_id not in df2.index:
                continue
            if refuse.method_pk == 1:
                df2.loc[refuse.farmer_id, "field_v"] = 1
            elif refuse.method_pk == 2:
                df2.loc[refuse.farmer_id, "field_y"] = 1

        for apply in applies:
            if apply.farmer_id not in df2.index:
                continue
            if apply.method_pk == 1:
                df2.loc[apply.farmer_id, "field_w"] = 1
                df2.loc[apply.farmer_id, "field_x"] = apply.result_pk
            elif apply.method_pk == 2:
                df2.loc[apply.farmer_id, "field_z"] = 1
                df2.loc[apply.farmer_id, "field_aa"] = apply.result_pk

        farmer_stats = FarmerStat.objects.filter(
            survey__page=1, survey__readonly=False, survey__is_invalid=False
        ).prefetch_related("survey")

        for stat in farmer_stats:
            is_senility = FarmerStat.get_is_senility(stat.survey)
            stratify = FarmerStat.get_stratify(stat.survey, is_senility)
            df2.loc[stat.survey.farmer_id, "field_ab"] = 2 if is_senility else 1
            df2.loc[stat.survey.farmer_id, "field_ac"] = stratify.code
            df2.loc[stat.survey.farmer_id, "field_ad"] = stratify.mix_magnification_factor

        df = (
            df1.join(df2, lsuffix="l", rsuffix="r").sort_values("field_a").reset_index()
        )

        self.write_rows_by_dataframe(sheet_name="戶檔", column_counts=30, dataframe=df)

    def process_sheet2(self):
        qs = (
            self.survey_qs.filter(page=1)
            .prefetch_related("businesses__farm_related_business")
            .values("farmer_id", "businesses__farm_related_business")
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("businesses__farm_related_business"),
            )
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="兼營農業相關事業", column_counts=2, queryset=qs)

    def process_sheet3(self):
        qs = (
            self.survey_qs.filter(page=1)
            .values("farmer_id")
            .prefetch_related(
                "crop_marketings",
                "crop_marketings__product",
                "crop_marketings__loss",
                "crop_marketings__unit",
            )
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("crop_marketings__product__code"),
                field_c=F("crop_marketings__name"),
                field_d=F("crop_marketings__land_number"),
                field_e=F("crop_marketings__land_area"),
                field_f=F("crop_marketings__plant_times"),
                field_g=F("crop_marketings__unit__code"),
                field_h=F("crop_marketings__year_sales"),
                field_i=F("crop_marketings__has_facility"),
                field_j=F("crop_marketings__loss__code"),
                count=Count("crop_marketings"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="農作物產銷情形", column_counts=10, queryset=qs)

    def process_sheet4(self):
        qs = (
            self.survey_qs.filter(page=1)
            .values("farmer_id")
            .prefetch_related(
                "livestock_marketings",
                "livestock_marketings__product",
                "livestock_marketings__loss",
                "livestock_marketings__contract",
            )
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("livestock_marketings__product__code"),
                field_c=F("livestock_marketings__name"),
                field_d=F("livestock_marketings__unit__code"),
                field_e=F("livestock_marketings__raising_number"),
                field_f=F("livestock_marketings__year_sales"),
                field_g=F("livestock_marketings__contract__code"),
                field_h=F("livestock_marketings__loss__code"),
                count=Count("livestock_marketings"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="畜禽產銷情形", column_counts=8, queryset=qs)

    def process_sheet5(self):
        qs = (
            self.survey_qs.filter(page=1)
            .values("farmer_id")
            .prefetch_related(
                "populations",
                "populations__relationship",
                "populations__gender",
                "populations__education_level",
                "populations__farmer_work_day",
                "population__life_style",
            )
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("populations__relationship__code"),
                field_c=F("populations__gender__code"),
                field_d=F("populations__birth_year"),
                field_e=F("populations__education_level__code"),
                field_f=F("populations__farmer_work_day__code"),
                field_g=F("populations__life_style__code"),
                count=Count("populations"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="人口檔", column_counts=7, queryset=qs)

    def process_sheet6(self):
        qs1 = (
            self.survey_qs.prefetch_related(
                "long_term_hires",
                "long_term_hires__avg_workday",
                "long_term_hires__work_type",
                "long_term_hires__number_workers",
            )
            .values("farmer_id", "long_term_hires")
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("long_term_hires__work_type__code"),
                field_c=Sum("long_term_hires__number_workers__count"),
                field_d=Sum(
                    Case(
                        When(
                            long_term_hires__number_workers__age_scope=1,
                            then="long_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_e=Sum(
                    Case(
                        When(
                            long_term_hires__number_workers__age_scope=2,
                            then="long_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_f=Sum(
                    Case(
                        When(
                            long_term_hires__number_workers__age_scope=3,
                            then="long_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_g=Cast(F("long_term_hires__avg_work_day"), IntegerField()),
                count=Count("long_term_hires"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        qs2 = (
            self.survey_qs.prefetch_related(
                "long_term_hires", "long_term_hires__months"
            )
            .values("farmer_id", "long_term_hires")
            .annotate(
                field_h=Sum(
                    Case(
                        When(long_term_hires__months=1, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_i=Sum(
                    Case(
                        When(long_term_hires__months=2, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_j=Sum(
                    Case(
                        When(long_term_hires__months=3, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_k=Sum(
                    Case(
                        When(long_term_hires__months=4, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_l=Sum(
                    Case(
                        When(long_term_hires__months=5, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_m=Sum(
                    Case(
                        When(long_term_hires__months=6, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_n=Sum(
                    Case(
                        When(long_term_hires__months=7, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_o=Sum(
                    Case(
                        When(long_term_hires__months=8, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_p=Sum(
                    Case(
                        When(long_term_hires__months=9, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_q=Sum(
                    Case(
                        When(long_term_hires__months=10, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_r=Sum(
                    Case(
                        When(long_term_hires__months=11, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_s=Sum(
                    Case(
                        When(long_term_hires__months=12, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                count=Count("long_term_hires"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        df1 = pandas.DataFrame(qs1).set_index("long_term_hires")
        df2 = pandas.DataFrame(qs2).set_index("long_term_hires")
        df = (
            df1.join(df2, lsuffix="l", rsuffix="r").sort_values("field_a").reset_index()
        )

        self.write_rows_by_dataframe(sheet_name="常僱", column_counts=19, dataframe=df)

    def process_sheet7(self):
        qs1 = (
            self.survey_qs.prefetch_related(
                "short_term_hires", "short_term_hires__avg_workday"
            )
            .values("farmer_id", "short_term_hires")
            .annotate(
                field_a=F("farmer_id"),
                field_b=Sum("short_term_hires__number_workers__count"),
                field_g=Coalesce(F("short_term_hires__avg_work_day"), -1),
                field_h=F("short_term_hires__month"),
                count=Count("short_term_hires"),
            )
            .filter(count__gt=0)
        )

        qs2 = (
            self.survey_qs.prefetch_related(
                "short_term_hires", "short_term_hires__number_workers"
            )
            .values("farmer_id", "short_term_hires")
            .annotate(
                field_c=Sum(
                    Case(
                        When(
                            short_term_hires__number_workers__age_scope=1,
                            then="short_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_d=Sum(
                    Case(
                        When(
                            short_term_hires__number_workers__age_scope=2,
                            then="short_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_e=Sum(
                    Case(
                        When(
                            short_term_hires__number_workers__age_scope=3,
                            then="short_term_hires__number_workers__count",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                count=Count("short_term_hires"),
            )
            .filter(count__gt=0)
        )

        qs3 = (
            self.survey_qs.prefetch_related(
                "short_term_hires",
                "short_term_hires__work_types",
            )
            .values("farmer_id", "short_term_hires")
            .annotate(
                field_f=StringAgg(
                    Cast("short_term_hires__work_types__code", CharField()),
                    delimiter=",",
                    distinct=True,
                ),
                count=Count("short_term_hires"),
            )
            .filter(count__gt=0)
        )

        df = pandas.DataFrame(qs1).set_index("short_term_hires")
        df2 = pandas.DataFrame(qs2).set_index("short_term_hires")
        df3 = pandas.DataFrame(qs3).set_index("short_term_hires")
        df = df.join(df2, lsuffix="l", rsuffix="r")
        df = df.join(df3, lsuffix="l", rsuffix="r").sort_values("field_a").reset_index()

        self.write_rows_by_dataframe(sheet_name="臨僱", column_counts=8, dataframe=df)

    def process_sheet8(self):
        qs = (
            self.survey_qs.prefetch_related("no_salary_hires")
            .values("farmer_id", "no_salary_hires")
            .annotate(
                field_a=F("farmer_id"),
                field_b=Sum("no_salary_hires__count"),
                field_c=F("no_salary_hires__month"),
                field_d=F("no_salary_hires__avg_work_day"),
                count=Count("no_salary_hires"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="不支薪", column_counts=4, queryset=qs)

    def process_sheet9(self):
        qs = (
            self.survey_qs.prefetch_related(
                "long_term_lacks",
                "long_term_lacks__months",
                "logn_term_lacks__work_type",
            )
            .values("farmer_id", "long_term_lacks")
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("long_term_lacks__work_type__code"),
                field_c=F("long_term_lacks__count"),
                field_d=F("long_term_lacks__avg_lack_day"),
                field_e=Sum(
                    Case(
                        When(long_term_lacks__months=1, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_f=Sum(
                    Case(
                        When(long_term_lacks__months=2, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_g=Sum(
                    Case(
                        When(long_term_lacks__months=3, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_h=Sum(
                    Case(
                        When(long_term_lacks__months=4, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_i=Sum(
                    Case(
                        When(long_term_lacks__months=5, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_j=Sum(
                    Case(
                        When(long_term_lacks__months=6, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_k=Sum(
                    Case(
                        When(long_term_lacks__months=7, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_l=Sum(
                    Case(
                        When(long_term_lacks__months=8, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_m=Sum(
                    Case(
                        When(long_term_lacks__months=9, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_n=Sum(
                    Case(
                        When(long_term_lacks__months=10, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_o=Sum(
                    Case(
                        When(long_term_lacks__months=11, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_p=Sum(
                    Case(
                        When(long_term_lacks__months=12, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                count=Count("long_term_lacks"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="常缺", column_counts=16, queryset=qs)

    def process_sheet10(self):
        qs = (
            self.survey_qs.prefetch_related(
                "short_term_lacks",
                "short_term_lacks__months",
                "short_term_lacks__work_type",
                "short_term_lacks__product",
            )
            .values("farmer_id", "short_term_lacks")
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("short_term_lacks__product__code"),
                field_c=F("short_term_lacks__name"),
                field_d=F("short_term_lacks__work_type__code"),
                field_e=F("short_term_lacks__count"),
                field_f=F("short_term_lacks__avg_lack_day"),
                field_g=Sum(
                    Case(
                        When(short_term_lacks__months=1, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_h=Sum(
                    Case(
                        When(short_term_lacks__months=2, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_i=Sum(
                    Case(
                        When(short_term_lacks__months=3, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_j=Sum(
                    Case(
                        When(short_term_lacks__months=4, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_k=Sum(
                    Case(
                        When(short_term_lacks__months=5, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_l=Sum(
                    Case(
                        When(short_term_lacks__months=6, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_m=Sum(
                    Case(
                        When(short_term_lacks__months=7, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_n=Sum(
                    Case(
                        When(short_term_lacks__months=8, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_o=Sum(
                    Case(
                        When(short_term_lacks__months=9, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_p=Sum(
                    Case(
                        When(short_term_lacks__months=10, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_q=Sum(
                    Case(
                        When(short_term_lacks__months=11, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                field_r=Sum(
                    Case(
                        When(short_term_lacks__months=12, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
                count=Count("short_term_lacks"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
        )

        self.write_rows_by_queryset(sheet_name="臨缺", column_counts=18, queryset=qs)

    def process_refuse_sheet(self, method, sheet_name):
        qs = (
            self.survey_qs.filter(page=1)
            .prefetch_related("subsidy__refuses", "subsidy__refuses__reason")
            .filter(subsidy__refuses__method=method.id)
            .annotate(
                field_a=F("farmer_id"),
                field_b=F("subsidy__refuses__reason"),
                count=Count("subsidy__refuses"),
            )
            .filter(count__gt=0)
            .order_by("farmer_id")
            .values("field_a", "field_b")
        )

        self.write_rows_by_queryset(sheet_name=sheet_name, column_counts=2, queryset=qs)

    def __call__(self, *args, **kwargs):

        methods = ApplyMethod.objects.order_by("id").all()

        self.process_sheet1()
        self.process_sheet2()
        self.process_sheet3()
        self.process_sheet4()
        self.process_sheet5()
        self.process_sheet6()
        self.process_sheet7()
        self.process_sheet8()
        self.process_sheet9()
        self.process_sheet10()
        for method, sheet_name in zip(
            methods, ["附帶調查_無申請人力團原因", "附帶調查_無申請農業外籍移工原因"]
        ):
            self.process_refuse_sheet(method, sheet_name)

        self.wb.save(*args, **kwargs)
