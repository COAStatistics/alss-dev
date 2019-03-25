from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, Management, ManagementType


class ModelTestCase(TestCase):
    """
    models: Management, Survey
    reference models : management-type.yaml
    data: management.yaml, survey.yaml
    main: Management associate other models, the one farmer has many managements.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'test/management.yaml', verbosity=0)
        call_command('loaddata', 'management-type.yaml', verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        management_list = Management.objects.all()
        self.assertEquals(len(management_list), 2)

        management_type_list = ManagementType.objects.all()
        self.assertEquals(len(management_type_list), 14)

    def test_create_business(self):
        survey_id = Survey.objects.get(id=3)
        management_type_a = ManagementType.objects.get(id=3)
        management_type_b = ManagementType.objects.get(id=9)

        management_list_before_size = len(Management.objects.all())

        #new value
        Management.objects.create(survey=survey_id)
        new_management = Management.objects.get(survey=survey_id)
        new_management.types.add(management_type_a, management_type_b)
        new_management.save()

        management_list_after_size = len(Management.objects.all())
        self.assertEquals(management_list_after_size, management_list_before_size+1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        management_list = Management.objects.filter(survey__id=1)
        self.assertEquals(management_list.count(), 0)

    def test_survey_delete_all(self):
        management_type_list_before_size = len(ManagementType.objects.all())
        Survey.objects.all().delete()
        management_list = Management.objects.all()
        management_type_list_after_size = len(ManagementType.objects.all())

        self.assertEquals(len(management_list), 0)
        self.assertEquals(management_type_list_after_size, management_type_list_before_size)