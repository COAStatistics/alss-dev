from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey, AddressMatch


class AddressMatchTestCase(TestCase):
    """
    models: AddressMatch, Survey
    reference models :
    data: s19-test-addressmatch.yaml, s19-test-survey.yaml
    main: AddressMatch associate survey, the one farmer has one address match info.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-test-addressmatch.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        address_match_list = AddressMatch.objects.all()
        self.assertEquals(len(address_match_list), 2)

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
