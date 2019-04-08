from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey, Subsidy


class SubsidyTestCase(TestCase):
    """
    models: Subsidy, Survey
    reference models :
    data: s19-test-subsidy.yaml, s19-test-survey.yaml
    main: Subsidy associate other models, the one farmer has one subsidy.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-test-subsidy.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        subsidy_list = Subsidy.objects.all()
        self.assertEquals(len(subsidy_list), 2)

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
