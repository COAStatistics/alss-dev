from . import TestCase, setup_fixtures
from apps.surveys18.models import Survey, Subsidy, Refuse, RefuseReason


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_survey(self):
        survey_id = Survey.objects.get(id=3)

        subsidy_list_before_size = Subsidy.objects.count()

        # new value
        new_subsidy = Subsidy.objects.create(survey=survey_id)
        new_subsidy.save()

        subsidy_list_after_size = Subsidy.objects.count()
        self.assertEquals(subsidy_list_after_size, subsidy_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        subsidy_list = Subsidy.objects.filter(survey__id=1)
        self.assertEquals(subsidy_list.count(), 0)

    def test_survey_delete_all(self):
        Survey.objects.all().delete()
        self.assertEquals(Subsidy.objects.count(), 0)
        self.assertEquals(Refuse.objects.count(), 0)
