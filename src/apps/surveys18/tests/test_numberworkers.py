from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, NumberWorkers, AgeScope, LongTermHire, Month, WorkType
from django.contrib.contenttypes.models import ContentType


class ModelTestCase(TestCase):
    """
    models: Survey, NumberWorkers
    reference models : AgeScope, NumberWorkers, LongTermHire
    data: numberworkers.yaml, survey.yaml, age-scope.yaml, longtermhire.yaml
    main: NumberWorkers associate other models.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'work-type.yaml', verbosity=0)
        call_command('loaddata', 'month.yaml', verbosity=0)
        call_command('loaddata', 'test/longtermhire.yaml', verbosity=0)
        call_command('loaddata', 'age-scope.yaml', verbosity=0)
        call_command('loaddata', 'test/numberworkers.yaml', verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        numberworkers_list = NumberWorkers.objects.all()
        self.assertEquals(len(numberworkers_list), 2)

    def test_create_population(self):
        content_type = ContentType.objects.get(app_label='surveys18', model='longtermhire')
        age_scope = AgeScope.objects.get(id=2)
        numberworkers_list_before_size = len(NumberWorkers.objects.all())

        #new value
        NumberWorkers.objects.create(value=20, content_type=content_type, object_id=3, age_scope=age_scope)

        numberworkers_list_after_size = len(NumberWorkers.objects.all())
        self.assertEquals(numberworkers_list_after_size, numberworkers_list_before_size+1)
