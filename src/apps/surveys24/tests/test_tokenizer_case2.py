from . import TestCase, setup_fixtures
from apps.surveys24.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):
        self.string = "6700500100020202++008芭樂#1004201100000080000020++++++++++"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        self.assertEqual(self.builder.survey.farmer_id, "670050010002")
        self.assertEqual(self.builder.survey.page, 2)
        self.assertEqual(self.builder.survey.total_pages, 2)

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEqual(len(self.builder.crop_marketing), 1)
        self.assertEqual(self.builder.crop_marketing[0].product, None)
        self.assertEqual(self.builder.crop_marketing[0].name, "芭樂")
        self.assertEqual(self.builder.crop_marketing[0].land_number, 1)
        self.assertEqual(self.builder.crop_marketing[0].land_area, 420)
        self.assertEqual(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEqual(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEqual(self.builder.crop_marketing[0].year_sales, 800000)
        self.assertEqual(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEqual(self.builder.crop_marketing[0].loss.code, 0)
