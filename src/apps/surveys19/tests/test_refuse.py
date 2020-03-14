from . import TestCase, setup_fixtures
from apps.surveys19.models import Survey, Subsidy, Refuse


class RefuseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

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
