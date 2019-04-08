from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import (
    Survey,
    NumberWorkers,
    AgeScope,
    LongTermHire,
    Month,
    WorkType,
)
from django.contrib.contenttypes.models import ContentType


class NumberWorkersTestCase(TestCase):
    """
    models: Survey, NumberWorkers, LongTermHire
    reference models : s19-age-scope.yaml, s19-month.yaml, s19-work-type.yaml
    data: s19-test-numberworkers.yaml, s19-test-survey.yaml, s19-test-longtermhire.yaml
    main: NumberWorkers associate other models.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-work-type.yaml", verbosity=0)
        call_command("loaddata", "s19-month.yaml", verbosity=0)
        call_command("loaddata", "s19-test-longtermhire.yaml", verbosity=0)
        call_command("loaddata", "s19-age-scope.yaml", verbosity=0)
        call_command("loaddata", "s19-test-numberworkers.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        numberworkers_list = NumberWorkers.objects.all()
        self.assertEquals(len(numberworkers_list), 2)

    def test_create_numberworkers(self):
        content_type = ContentType.objects.get(
            app_label="surveys19", model="longtermhire"
        )
        age_scope = AgeScope.objects.get(id=2)
        numberworkers_list_before_size = len(NumberWorkers.objects.all())

        # new value
        NumberWorkers.objects.create(
            count=20, content_type=content_type, object_id=3, age_scope=age_scope
        )

        numberworkers_list_after_size = len(NumberWorkers.objects.all())
        self.assertEquals(
            numberworkers_list_after_size, numberworkers_list_before_size + 1
        )
