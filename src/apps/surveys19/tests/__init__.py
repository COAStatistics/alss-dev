import pytest
from django.test import TestCase


@pytest.mark.s19
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command

    call_command("loaddata", "fixtures/surveys19/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/education-level.yaml", verbosity=0)
    call_command(
        "loaddata", "fixtures/surveys19/farm-related-business.yaml", verbosity=0
    )
    call_command("loaddata", "fixtures/surveys19/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/product-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/work-type.yaml", verbosity=0)

    call_command("loaddata", "fixtures/surveys19/test/survey.yaml", verbosity=0)

    call_command("loaddata", "fixtures/surveys19/test/addressmatch.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/annualincome.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/cropmarketing.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/landarea.yaml", verbosity=0)
    call_command(
        "loaddata", "fixtures/surveys19/test/livestockmarketing.yaml", verbosity=0
    )
    call_command("loaddata", "fixtures/surveys19/test/longtermhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/longtermlack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/nosalaryhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/numberworkers.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/phone.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/population.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/subsidy.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/refuse.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/shorttermhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys19/test/shorttermlack.yaml", verbosity=0)
