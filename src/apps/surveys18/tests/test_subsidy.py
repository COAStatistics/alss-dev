from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, Subsidy, RefuseReason


class ModelTestCase(TestCase):
    """
    models: Subsidy, Survey
    reference models : refuse-reason.yaml
    data: subsidy.yaml, survey.yaml
    main: Subsidy associate other models, the one farmer has one subsidy.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "test/survey.yaml", verbosity=0)
        call_command("loaddata", "refuse-reason.yaml", verbosity=0)
        call_command("loaddata", "test/subsidy.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        subsidy_list = Subsidy.objects.all()
        self.assertEquals(len(subsidy_list), 2)

        refuse_reason_list = RefuseReason.objects.all()
        self.assertEquals(len(refuse_reason_list), 3)

    def test_create_land_area(self):
        survey_id = Survey.objects.get(id=3)
        refuse_reason_a = RefuseReason.objects.get(id=1)
        refuse_reason_b = RefuseReason.objects.get(id=3)

        subsidy_list_before_size = len(Subsidy.objects.all())

        # new value
        Subsidy.objects.create(survey=survey_id)
        new_subsidy = Subsidy.objects.get(survey=survey_id)
        new_subsidy.reasons.add(refuse_reason_a, refuse_reason_b)
        new_subsidy.save()

        subsidy_list_after_size = len(Subsidy.objects.all())
        self.assertEquals(subsidy_list_after_size, subsidy_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        subsidy_list = Subsidy.objects.filter(survey__id=1)
        self.assertEquals(subsidy_list.count(), 0)

    def test_survey_delete_all(self):
        refuse_reason_list_before_size = len(RefuseReason.objects.all())
        Survey.objects.all().delete()
        subsidy_list = Subsidy.objects.all()
        refuse_reason_list_after_size = len(RefuseReason.objects.all())

        self.assertEquals(len(subsidy_list), 0)
        self.assertEquals(refuse_reason_list_after_size, refuse_reason_list_before_size)
