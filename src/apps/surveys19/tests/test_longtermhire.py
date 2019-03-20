from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey19, LongTermHire, WorkType


class LongTermHireTestCase(TestCase):
    """
    models: LongTermHire, Survey
    reference models : s19-work-type.yaml
    data: s19-test-longtermhire.yaml, s19-test-survey.yaml
    main: LongTermHire associate other models, the one farmer has many employee.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 's19-test-survey.yaml', verbosity=0)
        call_command('loaddata', 's19-work-type.yaml', verbosity=0)
        call_command('loaddata', 's19-test-longtermhire.yaml', verbosity=0)


    def test_loaddata(self):
        survey_list = Survey19.objects.all()
        self.assertEquals(len(survey_list), 3)

        longtermhire_list = LongTermHire.objects.all()
        self.assertEquals(len(longtermhire_list), 3)

        worktype_list = WorkType.objects.all()
        self.assertEquals(len(worktype_list), 7)

    def test_create_longtermhire(self):
        survey_id = Survey19.objects.get(id=3)
        work_type_code = WorkType.objects.get(id=4)

        longtermhire_list_before_size = len(LongTermHire.objects.all())

        #new value
        LongTermHire.objects.create(survey=survey_id, work_type=work_type_code, avg_work_day=30)

        longtermhire_list_after_size = len(LongTermHire.objects.all())
        self.assertEquals(longtermhire_list_after_size, longtermhire_list_before_size + 1)

    def test_survey_delete(self):
        Survey19.objects.filter(id=1).delete()
        longtermhire_list = LongTermHire.objects.filter(survey__id=1)
        self.assertEquals(longtermhire_list.count(), 0)

    def test_survey_delete_all(self):
        work_type_list_before_size = len(WorkType.objects.all())
        Survey19.objects.all().delete()
        longtermhire_list = LongTermHire.objects.all()
        work_type_list_after_size = len(WorkType.objects.all())

        self.assertEquals(len(longtermhire_list), 0)
        self.assertEquals(work_type_list_before_size, work_type_list_after_size)
