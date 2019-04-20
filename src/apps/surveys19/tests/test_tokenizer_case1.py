from django.test import TestCase
from .setup import setup_fixtures
from apps.surveys19.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    def setUp(self):
        self.string = "6700500100020101####林阿忠0912345678/##########3701屏東縣屏東市屏東路2號#台南#官田#6710+00250000000003001000000000100000001農所實驗#0000000000010010+101稻作(一期)#1004201100000002100021503桶柑#1003001100000000720020+F02泌乳牛#300009000000000500000F01肉牛#3001000000000015000031010000410020101080404+01110302000000101000000002220322000001001000000001+120040020010011010000000000005220040020010011111111111110010+0100900000500412130000000000000004010001005004142100000000000080+01002070050100+220011010000000000135140011111111111110080+香菇#A02130021100000000000060芒果#C06120010001100000000130+10121200011時間太忙#0#+稻受雨害影響#宋中積#宋會喬#0330"
        self.builder = Builder(self.string)
        self.builder.build_survey()

    def test_build_survey(self):
        self.assertEquals(self.builder.survey.farmer_id, "670050010002")
        self.assertEquals(self.builder.survey.page, 1)
        self.assertEquals(self.builder.survey.total_pages, 1)
        self.assertEquals(self.builder.survey.farmer_name, "林阿忠")
        self.assertEquals(self.builder.survey.origin_class, 37)
        self.assertEquals(self.builder.survey.note, "稻受雨害影響")
        self.assertEquals(self.builder.survey.period, 330)
        self.assertEquals(self.builder.survey.investigator, "宋中積")
        self.assertEquals(self.builder.survey.reviewer, "宋會喬")
        self.assertEquals(self.builder.survey.second, True)
        self.assertEquals(self.builder.survey.non_second, False)

        # check survey query string

    def test_build_phone(self):
        self.builder.build_phone()
        self.assertEquals(self.builder.phones[0].phone, "0912345678")
        # self.assertEquals(self.builder.phones[1].phone, "2991111")

    def test_build_address(self):
        self.builder.build_address()
        self.assertEquals(self.builder.address.match, False)
        self.assertEquals(self.builder.address.mismatch, True)
        self.assertEquals(self.builder.address.address, "屏東縣屏東市屏東路2號")

    def test_build_farm_location(self):
        self.builder.build_farm_location()
        self.assertEquals(self.builder.farm_location.city, "台南")
        self.assertEquals(self.builder.farm_location.town, "官田")
        self.assertEquals(self.builder.farm_location.code.code, "6710")

    def test_build_land_area(self):
        self.builder.build_land_area()
        self.assertEquals(len(self.builder.land_area), 3)

        self.assertEquals(self.builder.land_area[0].value, 250)
        self.assertEquals(self.builder.land_area[0].type.name, "可耕作地")
        self.assertEquals(self.builder.land_area[0].status.name, "自有")

        self.assertEquals(self.builder.land_area[1].value, 30)
        self.assertEquals(self.builder.land_area[1].type.name, "可耕作地")
        self.assertEquals(self.builder.land_area[1].status.name, "接受委託經營")

        self.assertEquals(self.builder.land_area[2].value, 1000)
        self.assertEquals(self.builder.land_area[2].type.name, "人工鋪面")
        self.assertEquals(self.builder.land_area[2].status.name, "自有")

    def test_build_business(self):
        self.builder.build_business()
        self.assertEquals(len(self.builder.business), 2)
        self.assertEquals(
            self.builder.business[0].farm_related_business.name, "無兼營農業相關事業"
        )
        self.assertEquals(self.builder.business[1].farm_related_business.name, "其他")
        self.assertEquals(self.builder.business[1].extra, "農所實驗")

    def test_build_management(self):
        self.builder.build_management()
        self.assertEquals(len(self.builder.survey.management_types.all()), 1)
        self.assertEquals(self.builder.survey.management_types.all()[0].name, "豬")

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEquals(len(self.builder.crop_marketing), 2)
        self.assertEquals(self.builder.crop_marketing[0].product.code, "101")
        self.assertEquals(self.builder.crop_marketing[0].name, "稻作(一期)")
        self.assertEquals(self.builder.crop_marketing[0].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[0].land_area, 420)
        self.assertEquals(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEquals(self.builder.crop_marketing[0].year_sales, 21000)
        self.assertEquals(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[0].loss.code, 1)

        self.assertEquals(self.builder.crop_marketing[1].product.code, "503")
        self.assertEquals(self.builder.crop_marketing[1].name, "桶柑")
        self.assertEquals(self.builder.crop_marketing[1].land_number, 1)
        self.assertEquals(self.builder.crop_marketing[1].land_area, 300)
        self.assertEquals(self.builder.crop_marketing[1].plant_times, 1)
        self.assertEquals(self.builder.crop_marketing[1].unit.code, 1)
        self.assertEquals(self.builder.crop_marketing[1].year_sales, 7200)
        self.assertEquals(self.builder.crop_marketing[1].has_facility, 0)
        self.assertEquals(self.builder.crop_marketing[1].loss.code, 0)

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        self.assertEquals(len(self.builder.livestock_marketing), 2)
        self.assertEquals(self.builder.livestock_marketing[0].product.code, "F02")
        self.assertEquals(self.builder.livestock_marketing[0].name, "泌乳牛")
        self.assertEquals(self.builder.livestock_marketing[0].unit.code, 3)
        self.assertEquals(self.builder.livestock_marketing[0].raising_number, 90)
        self.assertEquals(self.builder.livestock_marketing[0].year_sales, 5000)
        self.assertEquals(self.builder.livestock_marketing[0].contract.code, 0)
        self.assertEquals(self.builder.livestock_marketing[0].loss.code, 0)

        self.assertEquals(self.builder.livestock_marketing[1].product.code, "F01")
        self.assertEquals(self.builder.livestock_marketing[1].name, "肉牛")
        self.assertEquals(self.builder.livestock_marketing[1].unit.code, 3)
        self.assertEquals(self.builder.livestock_marketing[1].raising_number, 1000)
        self.assertEquals(self.builder.livestock_marketing[1].year_sales, 15000)
        self.assertEquals(self.builder.livestock_marketing[1].contract.code, 0)
        self.assertEquals(self.builder.livestock_marketing[1].loss.code, 3)

    def test_build_annual_income(self):
        self.builder.build_annual_income()
        self.assertEquals(len(self.builder.annual_income), 4)
        self.assertEquals(
            self.builder.annual_income[0].market_type.name, "農作物及其製品(含生產及加工)"
        )
        self.assertEquals(self.builder.annual_income[0].income_range.name, "500~未滿1000")
        self.assertEquals(
            self.builder.annual_income[1].market_type.name, "畜禽產品及其製品(含生產及加工)"
        )
        self.assertEquals(self.builder.annual_income[1].income_range.name, "500~未滿1000")
        self.assertEquals(self.builder.annual_income[2].market_type.name, "休閒、餐飲及相關事業")
        self.assertEquals(self.builder.annual_income[2].income_range.name, "75~未滿100")
        self.assertEquals(self.builder.annual_income[3].market_type.name, "銷售額總計")
        self.assertEquals(self.builder.annual_income[3].income_range.name, "500~未滿1000")

    def test_build_population_age(self):
        self.builder.build_population_age()
        self.assertEquals(len(self.builder.population_age), 4)
        self.assertEquals(self.builder.population_age[0].count, 1)
        self.assertEquals(self.builder.population_age[0].gender.name, "男")
        self.assertEquals(self.builder.population_age[0].age_scope.name, "未滿15歲")
        self.assertEquals(self.builder.population_age[1].count, 1)
        self.assertEquals(self.builder.population_age[1].gender.name, "女")
        self.assertEquals(self.builder.population_age[1].age_scope.name, "未滿15歲")
        self.assertEquals(self.builder.population_age[2].count, 4)
        self.assertEquals(self.builder.population_age[2].gender.name, "男")
        self.assertEquals(self.builder.population_age[2].age_scope.name, "滿15歲以上")
        self.assertEquals(self.builder.population_age[3].count, 4)
        self.assertEquals(self.builder.population_age[3].gender.name, "女")
        self.assertEquals(self.builder.population_age[3].age_scope.name, "滿15歲以上")

    def test_build_population(self):
        self.builder.build_population()
        self.assertEquals(len(self.builder.population), 2)
        self.assertEquals(self.builder.population[0].relationship.name, "戶長")
        self.assertEquals(self.builder.population[0].gender.name, "男")
        self.assertEquals(self.builder.population[0].birth_year, 30)
        self.assertEquals(self.builder.population[0].education_level.name, "小學及自修")
        self.assertEquals(self.builder.population[0].farmer_work_day.code, 7)
        self.assertEquals(self.builder.population[0].life_style.name, "自營農牧業工作")
        self.assertEquals(self.builder.population[1].relationship.name, "戶長之配偶")
        self.assertEquals(self.builder.population[1].gender.name, "女")
        self.assertEquals(self.builder.population[1].birth_year, 32)
        self.assertEquals(self.builder.population[1].education_level.name, "小學及自修")
        self.assertEquals(self.builder.population[1].farmer_work_day.code, 6)
        self.assertEquals(self.builder.population[1].life_style.name, "自營農牧業工作")

    def test_build_hire(self):
        self.builder.build_hire()
        self.assertEquals(self.builder.survey.non_hire, False)
        self.assertEquals(self.builder.survey.hire, True)

    def test_build_long_term_hire(self):
        self.builder.build_long_term_hire()
        self.assertEquals(len(self.builder.long_term_hire), 2)
        self.assertEquals(len(self.builder.long_term_hire[0].number_workers.all()), 3)
        self.assertEquals(len(self.builder.long_term_hire[0].months.all()), 2)
        self.assertEquals(self.builder.long_term_hire[0].avg_work_day, 0.5)
        self.assertEquals(len(self.builder.long_term_hire[1].number_workers.all()), 3)
        self.assertEquals(len(self.builder.long_term_hire[1].months.all()), 12)
        self.assertEquals(self.builder.long_term_hire[1].avg_work_day, 1)

    def test_build_short_term_hire(self):
        self.builder.build_short_term_hire()
        self.assertEquals(len(self.builder.short_term_hire), 2)
        self.assertEquals(len(self.builder.short_term_hire[0].number_workers.all()), 2)
        self.assertEquals(self.builder.short_term_hire[0].month.value, 1)
        self.assertEquals(self.builder.short_term_hire[0].avg_work_day, 0)
        self.assertEquals(len(self.builder.short_term_hire[1].number_workers.all()), 3)
        self.assertEquals(self.builder.short_term_hire[1].month.value, 4)
        self.assertEquals(self.builder.short_term_hire[1].avg_work_day, 8)

    def test_build_no_salary_hire(self):
        self.builder.build_no_salary_hire()
        self.assertEquals(len(self.builder.no_salary_hire), 2)
        self.assertEquals(self.builder.no_salary_hire[0].month.value, 1)
        self.assertEquals(self.builder.no_salary_hire[0].count, 2)
        self.assertEquals(self.builder.no_salary_hire[1].month.value, 7)
        self.assertEquals(self.builder.no_salary_hire[1].count, 5)

    def test_build_lack(self):
        self.builder.build_lack()
        self.assertEquals(len(self.builder.survey.lacks.all()), 1)

    def test_build_long_term_lack(self):
        self.builder.build_long_term_lack()
        self.assertEquals(len(self.builder.long_term_lack), 2)
        self.assertEquals(self.builder.long_term_lack[0].work_type.code, 22)
        self.assertEquals(self.builder.long_term_lack[0].count, 1)
        self.assertEquals(self.builder.long_term_lack[0].avg_lack_day, 13.5)
        self.assertEquals(len(self.builder.long_term_lack[0].months.all()), 2)
        self.assertEquals(self.builder.long_term_lack[1].work_type.code, 14)
        self.assertEquals(self.builder.long_term_lack[1].count, 1)
        self.assertEquals(self.builder.long_term_lack[1].avg_lack_day, 8)
        self.assertEquals(len(self.builder.long_term_lack[1].months.all()), 12)

    def test_build_short_term_lack(self):
        self.builder.build_short_term_lack()
        self.assertEquals(len(self.builder.short_term_lack), 2)
        self.assertEquals(self.builder.short_term_lack[0].name, "香菇")
        self.assertEquals(self.builder.short_term_lack[0].product, None)
        self.assertEquals(self.builder.short_term_lack[0].work_type.code, 13)
        self.assertEquals(self.builder.short_term_lack[0].count, 2)
        self.assertEquals(self.builder.short_term_lack[0].avg_lack_day, 6)
        self.assertEquals(len(self.builder.short_term_lack[0].months.all()), 2)
        self.assertEquals(len(self.builder.short_term_lack), 2)
        self.assertEquals(self.builder.short_term_lack[1].name, "芒果")
        self.assertEquals(self.builder.short_term_lack[1].product, None)
        self.assertEquals(self.builder.short_term_lack[1].work_type.code, 12)
        self.assertEquals(self.builder.short_term_lack[1].count, 1)
        self.assertEquals(self.builder.short_term_lack[1].avg_lack_day, 13)
        self.assertEquals(len(self.builder.short_term_lack[1].months.all()), 2)

    def test_build_subsidy(self):
        self.builder.build_subsidy()
        self.assertEquals(self.builder.subsidy.survey.farmer_id, "670050010002")
        self.assertEquals(self.builder.subsidy.none_subsidy, False)
        self.assertEquals(self.builder.subsidy.count, 12)
        self.assertEquals(self.builder.subsidy.month_delta, 12)
        self.assertEquals(self.builder.subsidy.day_delta, 0)
        self.assertEquals(len(self.builder.refuse), 2)
        self.assertEquals(self.builder.refuse[0].reason.name, "不知道此資訊")
        self.assertEquals(self.builder.refuse[0].extra, None)
        self.assertEquals(self.builder.refuse[1].reason.name, "沒有意願")
        self.assertEquals(self.builder.refuse[1].extra, "時間太忙")
