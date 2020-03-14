import pytest
from django.test import TestCase


@pytest.mark.s18
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command
    call_command("loaddata", "fixtures/surveys18/product-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/farm-related-business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/education-level.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/other-farm-work.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/work-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/refuse-reason.yaml", verbosity=0)

    call_command("loaddata", "fixtures/surveys18/test/survey.yaml", verbosity=0)

    call_command("loaddata", "fixtures/surveys18/test/addressmatch.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/annualincome.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/cropmarketing.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/landarea.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/livestockmarketing.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/longtermhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/longtermlack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/nosalaryhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/numberworkers.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/phone.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/population.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/subsidy.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/refuse.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/shorttermhire.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys18/test/shorttermlack.yaml", verbosity=0)
