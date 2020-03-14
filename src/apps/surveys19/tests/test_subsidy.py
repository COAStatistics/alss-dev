from . import TestCase, setup_fixtures
from apps.surveys19.models import Survey, Subsidy


class SubsidyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_subsidy(self):
        survey_id = Survey.objects.get(id=3)

        subsidy_list_before_size = len(Subsidy.objects.all())

        # new value
        Subsidy.objects.create(survey=survey_id)

        subsidy_list_after_size = len(Subsidy.objects.all())
        self.assertEquals(subsidy_list_after_size, subsidy_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        subsidy_list = Subsidy.objects.filter(survey__id=1)
        self.assertEquals(subsidy_list.count(), 0)

    def test_survey_delete_all(self):
        Survey.objects.all().delete()
        subsidy_list = Subsidy.objects.all()

        self.assertEquals(len(subsidy_list), 0)
