from django.core.management import call_command
from apps.surveys19.export import SurveyRelationGeneratorFactory

from . import TestCase


class ExportTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        call_command("loaddata", "fixtures/surveys19/test/export-sample.yaml", verbosity=0)

    def testFilter(self):
        factory = SurveyRelationGeneratorFactory()
        assert factory.surveys.count() == 5

        factory = SurveyRelationGeneratorFactory(excludes={'farmer_id': '9910001011'})
        assert factory.surveys.count() == 4

    def testRelationCount(self):
        factory = SurveyRelationGeneratorFactory()
        for relation in factory.lookup_tables:
            assert factory.check_relation(relation) is True

    def testGenerator(self):
        factory = SurveyRelationGeneratorFactory()
        generator = factory.export_generator()
        list(generator)
        assert factory.check_exhausted() is True
