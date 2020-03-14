from . import TestCase, setup_fixtures
from apps.surveys18.models import (
    Survey,
    NumberWorkers,
    AgeScope,
    LongTermHire,
    Month,
    WorkType,
)
from django.contrib.contenttypes.models import ContentType


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_population(self):
        content_type = ContentType.objects.get(
            app_label="surveys18", model="longtermhire"
        )
        age_scope = AgeScope.objects.get(id=2)
        numberworkers_list_before_size = len(NumberWorkers.objects.all())

        # new value
        NumberWorkers.objects.create(
            content_type=content_type, object_id=3, age_scope=age_scope
        )

        numberworkers_list_after_size = len(NumberWorkers.objects.all())
        self.assertEquals(
            numberworkers_list_after_size, numberworkers_list_before_size + 1
        )
