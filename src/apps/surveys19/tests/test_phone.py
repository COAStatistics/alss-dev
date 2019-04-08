from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys19.models import Survey, Phone


class PhoneTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

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
