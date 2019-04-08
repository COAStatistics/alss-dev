from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey, Phone


class PhoneTestCase(TestCase):
    """
    models: Phone, Survey
    reference models :
    data: s19-test-phone.yaml, s19-test-survey.yaml
    main: Phone associate survey, the one farmer has many phones.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-test-phone.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        phone_list = Phone.objects.all()
        self.assertEquals(len(phone_list), 3)

    def test_create_phone(self):
        survey_id = Survey.objects.get(id=3)
        phone_list_before_size = len(Phone.objects.all())

        # new value
        Phone.objects.create(survey=survey_id, phone=22222222)

        phone_list_after_size = len(Phone.objects.all())
        self.assertEquals(phone_list_after_size, phone_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        phone_list = Phone.objects.filter(survey__id=1)
        self.assertEquals(phone_list.count(), 0)
