from . import TestCase, setup_fixtures
from apps.surveys19.models import Survey, LongTermLack, WorkType, Month


class LongTermLackTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_longtermlack(self):
        survey_id = Survey.objects.get(id=3)
        month_a = Month.objects.get(id=8)
        month_b = Month.objects.get(id=9)
        month_c = Month.objects.get(id=10)
        work_type_code = WorkType.objects.get(id=5)

        longtermlack_list_before_size = len(LongTermLack.objects.all())

        # new value
        LongTermLack.objects.create(
            survey=survey_id, count=20, work_type=work_type_code, avg_lack_day=5.5
        )
        new_longtermlack = LongTermLack.objects.get(survey=survey_id)
        new_longtermlack.months.add(month_a, month_b, month_c)
        new_longtermlack.save()

        longtermlack_list_after_size = len(LongTermLack.objects.all())
        self.assertEquals(
            longtermlack_list_after_size, longtermlack_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        longtermlack_list = LongTermLack.objects.filter(survey=1)
        self.assertEquals(longtermlack_list.count(), 0)

    def test_survey_delete_all(self):
        month_list_before_size = len(Month.objects.all())
        Survey.objects.all().delete()
        longtermlack_list = LongTermLack.objects.all()
        month_list_after_size = len(Month.objects.all())

        self.assertEquals(len(longtermlack_list), 0)
        self.assertEquals(month_list_before_size, month_list_after_size)
