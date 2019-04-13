from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys19.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):
        self.string = "9800500100020202+++F01肉豬#300009000000050000000G02白肉雞#400100000000097500013+016209331000000000000010+++++++"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        self.assertEquals(self.builder.survey.farmer_id, "980050010002")
        self.assertEquals(self.builder.survey.page, 2)
        self.assertEquals(self.builder.survey.total_pages, 2)

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        self.assertEquals(len(self.builder.livestock_marketing), 2)
        self.assertEquals(self.builder.livestock_marketing[0].product.code, "F01")
        self.assertEquals(self.builder.livestock_marketing[0].name, "肉豬")
        self.assertEquals(self.builder.livestock_marketing[0].unit.code, 3)
        self.assertEquals(self.builder.livestock_marketing[0].raising_number, 90)
        self.assertEquals(self.builder.livestock_marketing[0].year_sales, 500000)
        self.assertEquals(self.builder.livestock_marketing[0].contract.code, 0)
        self.assertEquals(self.builder.livestock_marketing[0].loss.code, 0)

        self.assertEquals(self.builder.livestock_marketing[1].product.code, "G02")
        self.assertEquals(self.builder.livestock_marketing[1].name, "白肉雞")
        self.assertEquals(self.builder.livestock_marketing[1].unit.code, 4)
        self.assertEquals(self.builder.livestock_marketing[1].raising_number, 1000)
        self.assertEquals(self.builder.livestock_marketing[1].year_sales, 975000)
        self.assertEquals(self.builder.livestock_marketing[1].contract.code, 1)
        self.assertEquals(self.builder.livestock_marketing[1].loss.code, 3)

    def test_build_population(self):
        self.builder.build_population()
        self.assertEquals(len(self.builder.population), 1)
        self.assertEquals(self.builder.population[0].relationship.name, "戶長之孫子女及其配偶")
        self.assertEquals(self.builder.population[0].gender.name, "女")
        self.assertEquals(self.builder.population[0].birth_year, 93)
        self.assertEquals(self.builder.population[0].education_level.name, "國(初)中")
        self.assertEquals(self.builder.population[0].farmer_work_day.code, 1)
        self.assertEquals(self.builder.population[0].life_style.name, "學生")
