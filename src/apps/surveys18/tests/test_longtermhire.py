from . import TestCase, setup_fixtures
from apps.surveys18.models import Survey, LongTermHire, WorkType


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_longtermhire(self):
        survey_id = Survey.objects.get(id=3)
        work_type_code = WorkType.objects.get(id=4)

        longtermhire_list_before_size = len(LongTermHire.objects.all())

        # new value
        LongTermHire.objects.create(
            survey=survey_id, work_type=work_type_code, avg_work_day=30
        )

        longtermhire_list_after_size = len(LongTermHire.objects.all())
        self.assertEquals(
            longtermhire_list_after_size, longtermhire_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        longtermhire_list = LongTermHire.objects.filter(survey__id=1)
        self.assertEquals(longtermhire_list.count(), 0)

    def test_survey_delete_all(self):
        work_type_list_before_size = len(WorkType.objects.all())
        Survey.objects.all().delete()
        longtermhire_list = LongTermHire.objects.all()
        work_type_list_after_size = len(WorkType.objects.all())

        self.assertEquals(len(longtermhire_list), 0)
        self.assertEquals(work_type_list_before_size, work_type_list_after_size)
