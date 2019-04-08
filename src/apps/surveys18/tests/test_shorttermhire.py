from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys18.models import Survey, ShortTermHire, WorkType, Month


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_population(self):
        survey_id = Survey.objects.get(id=3)
        work_type_code_a = WorkType.objects.get(id=5)
        work_type_code_b = WorkType.objects.get(id=4)
        month = Month.objects.get(id=4)

        shorttermhire_list_before_size = len(ShortTermHire.objects.all())

        # new value
        ShortTermHire.objects.create(survey=survey_id, avg_work_day=20, month=month)
        new_shorttermhire = ShortTermHire.objects.get(survey=survey_id)
        new_shorttermhire.work_types.add(work_type_code_a, work_type_code_b)
        new_shorttermhire.save()

        shorttermhire_list_after_size = len(ShortTermHire.objects.all())
        self.assertEquals(
            shorttermhire_list_after_size, shorttermhire_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        shorttermhire_list = ShortTermHire.objects.filter(survey=1)
        self.assertEquals(shorttermhire_list.count(), 0)

    def test_survey_delete_all(self):
        month_list_before_size = len(Month.objects.all())
        Survey.objects.all().delete()
        shorttermhire_list = ShortTermHire.objects.all()
        month_list_after_size = len(Month.objects.all())

        self.assertEquals(len(shorttermhire_list), 0)
        self.assertEquals(month_list_before_size, month_list_after_size)
