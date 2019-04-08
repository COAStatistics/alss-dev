from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys18.models import Survey, AddressMatch


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_address_match(self):
        survey_id = Survey.objects.get(id=3)
        address_match_list_before_size = len(AddressMatch.objects.all())

        # new value
        AddressMatch.objects.create(
            survey=survey_id, match=True, mismatch=False, address=""
        )

        address_match_list_after_size = len(AddressMatch.objects.all())
        self.assertEquals(
            address_match_list_after_size, address_match_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        address_match_list = AddressMatch.objects.filter(survey__id=1)
        self.assertEquals(address_match_list.count(), 0)
