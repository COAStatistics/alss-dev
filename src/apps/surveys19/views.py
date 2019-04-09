import json

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from apps.surveys19.models import (
    Survey,
    CityTownCode,
    LandType,
    FarmRelatedBusiness,
    ManagementType,
    Product,
    Unit,
    Loss,
    Contract,
    MarketType,
    IncomeRange,
    AgeScope,
    Relationship,
    Gender,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    Lack,
    WorkType,
    RefuseReason,
    Month,
)


class Surveys2019Index(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    template_name = "surveys19/index.html"

    def get_context_data(self, **kwargs):
        context = super(Surveys2019Index, self).get_context_data(**kwargs)
        # template render objects
        context["farm_related_businesses"] = FarmRelatedBusiness.objects.all()
        context["management_types"] = ManagementType.objects.all()
        context["land_types"] = LandType.objects.all()
        context["income_ranges"] = IncomeRange.objects.all().order_by("minimum")
        context["market_types"] = MarketType.objects.all()
        context["genders"] = Gender.objects.all()
        context["population_age_scopes"] = AgeScope.objects.filter(group=2)
        context["hire_age_scopes"] = AgeScope.objects.filter(group=1)
        context["lacks"] = Lack.objects.all()

        # ui elements render objects
        context["contracts"] = Contract.objects.all()
        context["crop_products"] = Product.objects.filter(type=1)
        context["crop_losses"] = Loss.objects.filter(type=1)
        context["crop_units"] = Unit.objects.filter(type=1)
        context["livestock_products"] = Product.objects.filter(type=2)
        context["livestock_losses"] = Loss.objects.filter(type=2)
        context["livestock_units"] = Unit.objects.filter(type=2)
        context["education_levels"] = EducationLevel.objects.all()
        context["farmer_work_days"] = FarmerWorkDay.objects.all()
        context["genders"] = Gender.objects.all()
        context["months"] = Month.objects.all()
        context["relationships"] = Relationship.objects.all()
        context["life_styles"] = LifeStyle.objects.all()
        context["work_types"] = WorkType.objects.all()
        context["refuse_reasons"] = RefuseReason.objects.all()
        context["citytowncodes"] = CityTownCode.objects.all()

        # ui elements
        ui = {
            "cropmarketing": render_to_string(
                "surveys19/row-ui/crop-marketing.html", context
            ),
            "livestockmarketing": render_to_string(
                "surveys19/row-ui/livestock-marketing.html", context
            ),
            "population": render_to_string("surveys19/row-ui/population.html", context),
            "longtermhire": render_to_string(
                "surveys19/row-ui/long-term-hire.html", context
            ),
            "longtermlack": render_to_string(
                "surveys19/row-ui/long-term-lack.html", context
            ),
            "shorttermhire": render_to_string(
                "surveys19/row-ui/short-term-hire.html", context
            ),
            "shorttermlack": render_to_string(
                "surveys19/row-ui/short-term-lack.html", context
            ),
            "nosalaryhire": render_to_string(
                "surveys19/row-ui/no-salary-hire.html", context
            ),
        }
        context["ui"] = json.dumps(ui)
        context["fid"] = json.dumps(
            list(Survey.objects.values_list("farmer_id", flat=True).distinct())
        )

        return context
