from . import TestCase, setup_fixtures
from apps.surveys24.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.string = "1000903007800101####張素香/鄰居##056325823/##########0310#雲林#虎尾#0903+00200000000000000000000000100000000#10000000000000+102一期稻作#1002001100000033000020311綠肥作物#1002001n00000000000020+0200000002000000060303+10+++010001+++0000000000000000000000000000#0#++二期休耕。#謝孟娟#鄭艾倫#0327"
        cls.builder = Builder(cls.string)
        cls.builder.build_survey()

    def test_build_survey(self):
        self.assertEqual(self.builder.survey.farmer_id, "100090300780")
        self.assertEqual(self.builder.survey.page, 1)
        self.assertEqual(self.builder.survey.total_pages, 1)

        # check survey query string

    def test_build_phone(self):
        self.builder.build_phone()

    def test_build_address(self):
        self.builder.build_address()

    def test_build_farm_location(self):
        self.builder.build_farm_location()

    def test_build_land_area(self):
        self.builder.build_land_area()

    def test_build_business(self):
        self.builder.build_business()

    def test_build_management(self):
        self.builder.build_management()

    def test_build_farm_outsource(self):
        self.builder.build_farm_outsource()
        self.assertEqual(self.builder.survey.has_farm_outsource, False)
        self.assertEqual(self.builder.survey.non_has_farm_outsource, True)

    def test_build_lack(self):
        self.builder.build_lack()
        self.assertEqual(len(self.builder.survey.lacks.all()), 1)

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEqual(len(self.builder.crop_marketing), 2)
        self.assertEqual(self.builder.crop_marketing[0].product.code, "102")
        self.assertEqual(self.builder.crop_marketing[0].name, "一期稻作")
        self.assertEqual(self.builder.crop_marketing[0].land_number, 1)
        self.assertEqual(self.builder.crop_marketing[0].land_area, 200)
        self.assertEqual(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEqual(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEqual(self.builder.crop_marketing[0].year_sales, 330000)
        self.assertEqual(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEqual(self.builder.crop_marketing[0].loss.code, 0)

        self.assertEqual(self.builder.crop_marketing[1].product.code, "311")
        self.assertEqual(self.builder.crop_marketing[1].name, "綠肥作物")
        self.assertEqual(self.builder.crop_marketing[1].land_number, 1)
        self.assertEqual(self.builder.crop_marketing[1].land_area, 200)
        self.assertEqual(self.builder.crop_marketing[1].plant_times, 1)
        self.assertEqual(self.builder.crop_marketing[1].unit, None)
        self.assertEqual(self.builder.crop_marketing[1].year_sales, 0)
        self.assertEqual(self.builder.crop_marketing[1].has_facility, 0)
        self.assertEqual(self.builder.crop_marketing[1].loss.code, 0)
