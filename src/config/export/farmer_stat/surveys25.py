import os
import pandas
from django.db.models import Sum, Max, F, OuterRef, Subquery, Case, When, IntegerField, Q, Count

from django.db.models.functions import Coalesce
from apps.surveys25.models import Survey, ManagementType, Stratify, FarmerStat


class FarmerStatExporter113:
    def __init__(self):
        invalid_farmers = (
            Survey.objects.filter(Q(note__icontains="無效戶") | Q(is_invalid=True))
            .values_list("farmer_id", flat=True)
            .distinct()
        )
        valid_management_type_survey_ids = list(
            Survey.objects.annotate(m_count=Count("management_types"))
            .filter(m_count=1)
            .values_list("id", flat=True)
        )
        self.survey_qs = (Survey.objects.filter(
            readonly=False, id__in=valid_management_type_survey_ids,
        ).exclude(
            farmer_id__in=invalid_farmers,
        ))

    @staticmethod
    def get_stratify_df():
        df = pandas.DataFrame(columns=["id", "stratify", "origin_magnification_factor", "mix_magnification_factor"])
        for i, obj in enumerate(Stratify.objects.all()):
            df.loc[i] = [
                obj.pk,
                obj.code,
                obj.origin_magnification_factor if obj.origin_sample_count > 0 else "-",
                obj.mix_magnification_factor if obj.mix_sample_count > 0 else "-",
            ]
        return df

    def get_farmer_df(self):
        management_types = ManagementType.objects.filter(
            surveys__page=1, surveys__readonly=False, surveys=OuterRef("pk")
        )

        qs = (
            self.survey_qs.filter(page=1)
            .prefetch_related(
                "land_areas",
                "farm_location__code",
                "farmer_stat",
                "crop_marketings",
                "livestock_marketings",
            )
            .values("farmer_id")
            .annotate(
                origin_class=F("origin_class"),
                region_code=F("farm_location__code__region"),
                city_code=F("farm_location__code__code"),
                product_type=Subquery(management_types.values("type")[:1]),
                management_type=Subquery(management_types.values("code")[:1]),
                stratify=Coalesce(F("farmer_stat__stratify"), -1),
                before_group=Case(
                    When(origin_class__lt=101, then=1),
                    default=2,
                    output_field=IntegerField(),
                ),
                after_group=Case(
                    When(farmer_stat__is_senility=True, then=2),
                    When(farmer_stat__is_senility=False, then=1),
                    output_field=IntegerField(),
                ),
            )
        )
        df = pandas.DataFrame(qs)
        df["city_code"] = df["city_code"].apply(lambda x: x.zfill(4)[:2])
        return df

    def get_year_sales_df(self):
        qs = (
            self.survey_qs.prefetch_related("crop_marketings", "livestock_marketings")
            .values("farmer_id")
            .annotate(
                crop_year_sales=Coalesce(Sum("crop_marketings__year_sales"), 0),
                livestock_year_sales=Coalesce(
                    Sum("livestock_marketings__year_sales"), 0
                ),
            )
        )
        df = pandas.DataFrame(qs)
        df["total_year_sales"] = df["crop_year_sales"] + df["livestock_year_sales"]
        return df

    def get_land_area_df(self):
        qs = (
            self.survey_qs.values("farmer_id", "crop_marketings__land_number")
            .order_by()
            .annotate(land_area=Max("crop_marketings__land_area"))
        )
        df = pandas.DataFrame(qs)
        df = df.groupby("farmer_id", as_index=False).agg({"land_area": "sum"})
        return df

    def __call__(self, *args, **kwargs):
        assert FarmerStat.objects.count() > 0, "FarmerStats are not yet resolved."

        farmer_df = self.get_farmer_df()
        stratify_df = self.get_stratify_df()
        year_sales_df = self.get_year_sales_df()
        land_areas_df = self.get_land_area_df()

        # Join dataframes
        farmer_df = farmer_df.set_index("stratify").join(stratify_df.set_index("id"))
        farmer_df = farmer_df.set_index("farmer_id").join(
            year_sales_df.set_index("farmer_id")
        )
        farmer_df = farmer_df.join(land_areas_df.set_index("farmer_id"))

        # 把 land_area 或 stratify 為 NaN 的列整批丟掉
        farmer_df = farmer_df.dropna(subset=["land_area", "stratify"])

        # Formatting dataframe
        farmer_df = farmer_df.astype({"stratify": int, "land_area": int}).sort_index()
        farmer_df.index.name = "農戶編號"
        farmer_df.rename(
            {
                "region_code": "四區代碼",
                "city_code": "縣市代碼",
                "product_type": "農1畜2",
                "management_type": "主要經營型態",
                "stratify": "層別",
                "magnification_factor": "擴大係數",
                "crop_year_sales": "農耕銷售額",
                "livestock_year_sales": "畜禽銷售額",
                "total_year_sales": "銷售額總計",
                "land_area": "耕地面積（公畝）",
                "origin_class": "原層別",
                "before_group": "原非高齡1高齡2",
                "after_group": "事後非高齡1高齡2",
                "origin_magnification_factor": "純擴大係數",
                "mix_magnification_factor": "混和擴大係數"
            },
            axis=1,
            inplace=True,
        )

        # Export dataframe
        farmer_df.to_excel(*args, **kwargs)
