import pytest
from django.test import TestCase


@pytest.mark.s25
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command

    call_command("loaddata", "fixtures/surveys25/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/education-level.yaml", verbosity=0)
    call_command(
        "loaddata", "fixtures/surveys25/farm-related-business.yaml", verbosity=0
    )
    call_command("loaddata", "fixtures/surveys25/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/work-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/apply-result.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/apply-method.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/hire-channel-item.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/lack-response-item.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys25/max-hourly-pay-item.yaml", verbosity=0)
