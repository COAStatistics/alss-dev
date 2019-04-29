from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys19.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):
        self.string = "1000903007800101####張素香#056325823/##########0310#雲林#虎尾#0903+00200000000000000000000000100000000#1000000000000001+438蕃茄（２期）#1002001100000033000020438蕃茄（１期）#1002001n00000000000020+0200000002000000060303+01120460000100010000000023202010000000000001000321044000001001000000004510710010000000001000055107300100000100000000652068100000000000100010+++0001+++10121200011缺工２．０計畫工資較高#0#+二期休耕。#謝孟娟#鄭艾倫#03270040"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        self.assertEquals(self.builder.survey.farmer_id, "100090300780")
        self.assertEquals(self.builder.survey.page, 1)
        self.assertEquals(self.builder.survey.total_pages, 1)

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

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEquals(len(self.builder.crop_marketing), 2)
        self.assertEquals(self.builder.crop_marketing[0].product.code, "438")
        self.assertEquals(self.builder.crop_marketing[0].name, "蕃茄（２期）")
        self.assertEquals(self.builder.crop_marketing[0].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[0].land_area, 200)
        self.assertEquals(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEquals(self.builder.crop_marketing[0].year_sales, 330000)
        self.assertEquals(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[0].loss.code, 0)

        self.assertEquals(self.builder.crop_marketing[1].product.code, "438")
        self.assertEquals(self.builder.crop_marketing[1].name, "蕃茄（１期）")
        self.assertEquals(self.builder.crop_marketing[1].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[1].land_area, 200)
        self.assertEquals(self.builder.crop_marketing[1].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[1].unit, None)
        self.assertEquals(self.builder.crop_marketing[1].year_sales, 0)
        self.assertEquals(self.builder.crop_marketing[1].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[1].loss.code, 0)

    def test_build_subsidy(self):
        self.builder.build_subsidy()
        self.assertEquals(self.builder.subsidy.survey.farmer_id, "100090300780")
        self.assertEquals(self.builder.subsidy.none_subsidy, False)
        self.assertEquals(self.builder.subsidy.count, 12)
        self.assertEquals(self.builder.subsidy.month_delta, 12)
        self.assertEquals(self.builder.subsidy.day_delta, 0)
        self.assertEquals(len(self.builder.refuse), 2)
        self.assertEquals(self.builder.refuse[0].reason.name, "不知道此資訊")
        self.assertEquals(self.builder.refuse[0].extra, None)
        self.assertEquals(self.builder.refuse[1].reason.name, "沒有意願")
        self.assertEquals(self.builder.refuse[1].extra, "缺工２．０計畫工資較高")
