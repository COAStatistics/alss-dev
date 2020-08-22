import pytest
from django.test import TestCase


@pytest.mark.s20
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command
    call_command("loaddata", "fixtures/surveys20/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/education-level.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/farm-related-business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys20/work-type.yaml", verbosity=0)
