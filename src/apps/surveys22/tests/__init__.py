import pytest
from django.test import TestCase


@pytest.mark.s22
class TestCase(TestCase):
    pass


def setup_fixtures():
    from django.core.management import call_command
    call_command("loaddata", "fixtures/surveys22/age-scope.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/city-town-code.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/contract.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/education-level.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/farm-related-business.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/farmer-work-day.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/gender.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/income-range.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/lack.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/land-status.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/unit.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/land-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/life-style.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/loss.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/management-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/market-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/month.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/product.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/refuse-reason.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/relationship.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/work-type.yaml", verbosity=0)
    call_command("loaddata", "fixtures/surveys22/subsidy-result.yaml", verbosity=0)
