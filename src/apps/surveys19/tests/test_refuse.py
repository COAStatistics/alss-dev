from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey, Subsidy, Refuse, RefuseReason


class RefuseTestCase(TestCase):
    """
    models: Refuse, Survey
    reference models : s19-refuse-reason.yaml
    data: s19-test-subsidy.yaml, s19-test-survey.yaml, s19-test-refuse.yaml
    main: Subsidy associate other models, the one farmer has one subsidy.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-test-subsidy.yaml", verbosity=0)
        call_command("loaddata", "s19-refuse-reason.yaml", verbosity=0)
        call_command("loaddata", "s19-test-refuse.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        subsidy_list = Subsidy.objects.all()
        self.assertEquals(len(subsidy_list), 2)

        refuse_list = Refuse.objects.all()
        self.assertEquals(len(refuse_list), 2)

        refusereason_list = RefuseReason.objects.all()
        self.assertEquals(len(refusereason_list), 3)

    def test_create_refuse(self):
        subsidy_id = Subsidy.objects.first()

        refuse_list_before_size = len(Refuse.objects.all())

        # new value
        Refuse.objects.create(subsidy=subsidy_id)

        refuse_list_after_size = len(Refuse.objects.all())
        self.assertEquals(refuse_list_after_size, refuse_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        refuse_list = Refuse.objects.filter(subsidy__id=1)
        self.assertEquals(refuse_list.count(), 0)

    def test_survey_delete_all(self):
        Survey.objects.all().delete()
        refuse_list = Refuse.objects.all()

        self.assertEquals(len(refuse_list), 0)
