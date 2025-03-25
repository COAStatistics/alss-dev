from . import TestCase, setup_fixtures
from apps.surveys25.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):
        self.string = "9800500100020202+++F01肉豬#300009000000050000000G02白肉雞#400100000000097500013+016209331000000000000010++++++++"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        self.assertEqual(self.builder.survey.farmer_id, "980050010002")
        self.assertEqual(self.builder.survey.page, 2)
        self.assertEqual(self.builder.survey.total_pages, 2)

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        self.assertEqual(len(self.builder.livestock_marketing), 2)
        self.assertEqual(self.builder.livestock_marketing[0].product.code, "F01")
        self.assertEqual(self.builder.livestock_marketing[0].name, "肉豬")
        self.assertEqual(self.builder.livestock_marketing[0].unit.code, 3)
        self.assertEqual(self.builder.livestock_marketing[0].raising_number, 90)
        self.assertEqual(self.builder.livestock_marketing[0].year_sales, 500000)
        self.assertEqual(self.builder.livestock_marketing[0].contract.code, 0)
        self.assertEqual(self.builder.livestock_marketing[0].loss.code, 0)

        self.assertEqual(self.builder.livestock_marketing[1].product.code, "G02")
        self.assertEqual(self.builder.livestock_marketing[1].name, "白肉雞")
        self.assertEqual(self.builder.livestock_marketing[1].unit.code, 4)
        self.assertEqual(self.builder.livestock_marketing[1].raising_number, 1000)
        self.assertEqual(self.builder.livestock_marketing[1].year_sales, 975000)
        self.assertEqual(self.builder.livestock_marketing[1].contract.code, 1)
        self.assertEqual(self.builder.livestock_marketing[1].loss.code, 3)

    def test_build_population(self):
        self.builder.build_population()
        self.assertEqual(len(self.builder.population), 1)
        self.assertEqual(self.builder.population[0].relationship.name, "經濟戶長之孫子女及其配偶")
        self.assertEqual(self.builder.population[0].gender.name, "女")
        self.assertEqual(self.builder.population[0].birth_year, 93)
        self.assertEqual(self.builder.population[0].education_level.name, "國(初)中")
        self.assertEqual(self.builder.population[0].farmer_work_day.code, 1)
        self.assertEqual(self.builder.population[0].life_style.name, "求學或準備升學")
