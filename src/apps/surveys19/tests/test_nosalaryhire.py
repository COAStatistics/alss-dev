from . import TestCase, setup_fixtures
from apps.surveys19.models import Survey, NoSalaryHire, Month


class NoSalaryHireTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_nosalaryhire(self):
        survey_id = Survey.objects.get(id=3)
        month = Month.objects.get(id=12)

        nosalaryhire_list_before_size = len(NoSalaryHire.objects.all())

        # new value
        NoSalaryHire.objects.create(survey=survey_id, count=15, month=month)

        nosalaryhire_list_after_size = len(NoSalaryHire.objects.all())
        self.assertEquals(
            nosalaryhire_list_after_size, nosalaryhire_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        nosalaryhire_list = NoSalaryHire.objects.filter(survey=1)
        self.assertEquals(nosalaryhire_list.count(), 0)

    def test_survey_delete_all(self):
        month_list_before_size = len(Month.objects.all())
        Survey.objects.all().delete()
        nosalaryhire_list = NoSalaryHire.objects.all()
        month_list_after_size = len(Month.objects.all())

        self.assertEquals(len(nosalaryhire_list), 0)
        self.assertEquals(month_list_before_size, month_list_after_size)
