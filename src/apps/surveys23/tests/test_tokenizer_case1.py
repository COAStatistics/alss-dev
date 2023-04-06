from . import TestCase, setup_fixtures
from apps.surveys23.builder.tokenizer import Builder


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_fixtures()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.string = "6700500100020101####林阿忠/本人#0912345678/##########3701屏東縣屏東市屏東路2號#台南#官田#6710+00250000000003001000000000100000001農所實驗#00000000000100+102稻作(一期)#1004201100000002100021503桶柑#1003001100000000720020+F02泌乳牛#300009000000000500000F01肉牛#300100000000001500003101000041010020101080404+01110302000000101000000002220322000001001000000001+120040020010011010000000000005220040020010011111111111110010+0100900000500412130000000000000004010001005004142100000000000080+0100200170700500090100+220011010000000000135140011111111111110080+香菇#A02130021100000000000060芒果#C06120010001100000000130+01010000100010000000001000000010100#0#1美國農業局#01+稻受雨害影響#宋中積#宋會喬#0330"
        cls.builder = Builder(cls.string)
        cls.builder.build_survey()

    def test_build_survey(self):
        self.assertEqual(self.builder.survey.farmer_id, "670050010002")
        self.assertEqual(self.builder.survey.page, 1)
        self.assertEqual(self.builder.survey.total_pages, 1)
        self.assertEqual(self.builder.survey.farmer_name, "林阿忠")
        self.assertEqual(self.builder.survey.interviewee_relationship, "本人")
        self.assertEqual(self.builder.survey.origin_class, 37)
        self.assertEqual(self.builder.survey.note, "稻受雨害影響")
        self.assertEqual(self.builder.survey.period, 330)
        self.assertEqual(self.builder.survey.investigator, "宋中積")
        self.assertEqual(self.builder.survey.reviewer, "宋會喬")
        # TODO: remove second and non_second
        self.assertEqual(self.builder.survey.main_income_source, True)
        self.assertEqual(self.builder.survey.non_main_income_source, False)
        self.assertEqual(self.builder.survey.known_subsidy, True)
        self.assertEqual(self.builder.survey.non_known_subsidy, False)

        # check survey query string

    def test_build_phone(self):
        self.builder.build_phone()
        self.assertEqual(self.builder.phones[0].phone, "0912345678")
        # self.assertEqual(self.builder.phones[1].phone, "2991111")

    def test_build_address(self):
        self.builder.build_address()
        self.assertEqual(self.builder.address.match, False)
        self.assertEqual(self.builder.address.mismatch, True)
        self.assertEqual(self.builder.address.address, "屏東縣屏東市屏東路2號")

    def test_build_farm_location(self):
        self.builder.build_farm_location()
        self.assertEqual(self.builder.farm_location.city, "台南")
        self.assertEqual(self.builder.farm_location.town, "官田")
        self.assertEqual(self.builder.farm_location.code.code, "6710")

    def test_build_land_area(self):
        self.builder.build_land_area()
        self.assertEqual(len(self.builder.land_area), 3)

        self.assertEqual(self.builder.land_area[0].value, 250)
        self.assertEqual(self.builder.land_area[0].type.name, "可耕作地")
        self.assertEqual(self.builder.land_area[0].status.name, "自有")

        self.assertEqual(self.builder.land_area[1].value, 30)
        self.assertEqual(self.builder.land_area[1].type.name, "可耕作地")
        self.assertEqual(self.builder.land_area[1].status.name, "接受委託經營")

        self.assertEqual(self.builder.land_area[2].value, 1000)
        self.assertEqual(self.builder.land_area[2].type.name, "人工鋪面")
        self.assertEqual(self.builder.land_area[2].status.name, "自有")

    def test_build_business(self):
        self.builder.build_business()
        self.assertEqual(len(self.builder.business), 2)
        self.assertEqual(
            self.builder.business[0].farm_related_business.name, "無兼營農業相關事業"
        )
        self.assertEqual(self.builder.business[1].farm_related_business.name, "其他")
        self.assertEqual(self.builder.business[1].extra, "農所實驗")

    def test_build_management(self):
        self.builder.build_management()
        self.assertEqual(len(self.builder.survey.management_types.all()), 1)
        self.assertEqual(self.builder.survey.management_types.all()[0].name, "豬")

    def test_build_crop_marketing(self):
        self.builder.build_crop_marketing()
        self.assertEqual(len(self.builder.crop_marketing), 2)
        self.assertEqual(self.builder.crop_marketing[0].product.code, "102")
        self.assertEqual(self.builder.crop_marketing[0].name, "稻作(一期)")
        self.assertEqual(self.builder.crop_marketing[0].land_number, 1)
        self.assertEqual(self.builder.crop_marketing[0].land_area, 420)
        self.assertEqual(self.builder.crop_marketing[0].plant_times, 1)
        self.assertEqual(self.builder.crop_marketing[0].unit.code, 1)
        self.assertEqual(self.builder.crop_marketing[0].year_sales, 21000)
        self.assertEqual(self.builder.crop_marketing[0].has_facility, 0)
        self.assertEqual(self.builder.crop_marketing[0].loss.code, 1)

        self.assertEqual(self.builder.crop_marketing[1].product.code, "503")
        self.assertEqual(self.builder.crop_marketing[1].name, "桶柑")
        self.assertEqual(self.builder.crop_marketing[1].land_number, 1)
        self.assertEqual(self.builder.crop_marketing[1].land_area, 300)
        self.assertEqual(self.builder.crop_marketing[1].plant_times, 1)
        self.assertEqual(self.builder.crop_marketing[1].unit.code, 1)
        self.assertEqual(self.builder.crop_marketing[1].year_sales, 7200)
        self.assertEqual(self.builder.crop_marketing[1].has_facility, 0)
        self.assertEqual(self.builder.crop_marketing[1].loss.code, 0)

    def test_build_livestock_marketing(self):
        self.builder.build_livestock_marketing()
        self.assertEqual(len(self.builder.livestock_marketing), 2)
        self.assertEqual(self.builder.livestock_marketing[0].product.code, "F02")
        self.assertEqual(self.builder.livestock_marketing[0].name, "泌乳牛")
        self.assertEqual(self.builder.livestock_marketing[0].unit.code, 3)
        self.assertEqual(self.builder.livestock_marketing[0].raising_number, 90)
        self.assertEqual(self.builder.livestock_marketing[0].year_sales, 5000)
        self.assertEqual(self.builder.livestock_marketing[0].contract.code, 0)
        self.assertEqual(self.builder.livestock_marketing[0].loss.code, 0)

        self.assertEqual(self.builder.livestock_marketing[1].product.code, "F01")
        self.assertEqual(self.builder.livestock_marketing[1].name, "肉牛")
        self.assertEqual(self.builder.livestock_marketing[1].unit.code, 3)
        self.assertEqual(self.builder.livestock_marketing[1].raising_number, 1000)
        self.assertEqual(self.builder.livestock_marketing[1].year_sales, 15000)
        self.assertEqual(self.builder.livestock_marketing[1].contract.code, 0)
        self.assertEqual(self.builder.livestock_marketing[1].loss.code, 3)

    def test_build_annual_income(self):
        self.builder.build_annual_income()
        self.assertEqual(len(self.builder.annual_income), 4)
        self.assertEqual(
            self.builder.annual_income[0].market_type.name, "農作物及其製品(含生產及加工)"
        )
        self.assertEqual(self.builder.annual_income[0].income_range.name, "500~未滿1000")
        self.assertEqual(
            self.builder.annual_income[1].market_type.name, "畜禽產品及其製品(含生產及加工)"
        )
        self.assertEqual(self.builder.annual_income[1].income_range.name, "500~未滿1000")
        self.assertEqual(self.builder.annual_income[2].market_type.name, "休閒、餐飲及相關事業")
        self.assertEqual(self.builder.annual_income[2].income_range.name, "70~未滿100")
        self.assertEqual(self.builder.annual_income[3].market_type.name, "銷售額總計")
        self.assertEqual(self.builder.annual_income[3].income_range.name, "500~未滿1000")

    def test_build_population_age(self):
        self.builder.build_population_age()
        self.assertEqual(len(self.builder.population_age), 4)
        self.assertEqual(self.builder.population_age[0].count, 1)
        self.assertEqual(self.builder.population_age[0].gender.name, "男")
        self.assertEqual(self.builder.population_age[0].age_scope.name, "未滿15歲")
        self.assertEqual(self.builder.population_age[1].count, 1)
        self.assertEqual(self.builder.population_age[1].gender.name, "女")
        self.assertEqual(self.builder.population_age[1].age_scope.name, "未滿15歲")
        self.assertEqual(self.builder.population_age[2].count, 4)
        self.assertEqual(self.builder.population_age[2].gender.name, "男")
        self.assertEqual(self.builder.population_age[2].age_scope.name, "滿15歲以上")
        self.assertEqual(self.builder.population_age[3].count, 4)
        self.assertEqual(self.builder.population_age[3].gender.name, "女")
        self.assertEqual(self.builder.population_age[3].age_scope.name, "滿15歲以上")

    def test_build_population(self):
        self.builder.build_population()
        self.assertEqual(len(self.builder.population), 2)
        self.assertEqual(self.builder.population[0].relationship.name, "經濟戶長")
        self.assertEqual(self.builder.population[0].gender.name, "男")
        self.assertEqual(self.builder.population[0].birth_year, 30)
        self.assertEqual(self.builder.population[0].education_level.name, "小學及自修")
        self.assertEqual(self.builder.population[0].farmer_work_day.code, 7)
        self.assertEqual(self.builder.population[0].life_style.name, "自營農牧業工作")
        self.assertEqual(self.builder.population[1].relationship.name, "經濟戶長之配偶")
        self.assertEqual(self.builder.population[1].gender.name, "女")
        self.assertEqual(self.builder.population[1].birth_year, 32)
        self.assertEqual(self.builder.population[1].education_level.name, "小學及自修")
        self.assertEqual(self.builder.population[1].farmer_work_day.code, 6)
        self.assertEqual(self.builder.population[1].life_style.name, "自營農牧業工作")

    def test_build_hire(self):
        self.builder.build_hire()
        self.assertEqual(self.builder.survey.non_hire, False)
        self.assertEqual(self.builder.survey.hire, True)

    def test_build_long_term_hire(self):
        self.builder.build_long_term_hire()
        self.assertEqual(len(self.builder.long_term_hire), 2)
        self.assertEqual(len(self.builder.long_term_hire[0].number_workers.all()), 3)
        self.assertEqual(len(self.builder.long_term_hire[0].months.all()), 2)
        self.assertEqual(self.builder.long_term_hire[0].avg_work_day, 0.5)
        self.assertEqual(len(self.builder.long_term_hire[1].number_workers.all()), 3)
        self.assertEqual(len(self.builder.long_term_hire[1].months.all()), 12)
        self.assertEqual(self.builder.long_term_hire[1].avg_work_day, 1)

    def test_build_short_term_hire(self):
        self.builder.build_short_term_hire()
        self.assertEqual(len(self.builder.short_term_hire), 2)
        self.assertEqual(len(self.builder.short_term_hire[0].number_workers.all()), 2)
        self.assertEqual(self.builder.short_term_hire[0].month.value, 1)
        self.assertEqual(self.builder.short_term_hire[0].avg_work_day, 0)
        self.assertEqual(len(self.builder.short_term_hire[1].number_workers.all()), 3)
        self.assertEqual(self.builder.short_term_hire[1].month.value, 4)
        self.assertEqual(self.builder.short_term_hire[1].avg_work_day, 8)

    def test_build_no_salary_hire(self):
        self.builder.build_no_salary_hire()
        self.assertEqual(len(self.builder.no_salary_hire), 2)
        self.assertEqual(self.builder.no_salary_hire[0].month.value, 1)
        self.assertEqual(self.builder.no_salary_hire[0].count, 2)
        self.assertEqual(self.builder.no_salary_hire[0].avg_work_day, 1.7)
        self.assertEqual(self.builder.no_salary_hire[1].month.value, 7)
        self.assertEqual(self.builder.no_salary_hire[1].count, 5)
        self.assertEqual(self.builder.no_salary_hire[1].avg_work_day, 0.9)

    def test_build_lack(self):
        self.builder.build_lack()
        self.assertEqual(len(self.builder.survey.lacks.all()), 1)

    def test_build_long_term_lack(self):
        self.builder.build_long_term_lack()
        self.assertEqual(len(self.builder.long_term_lack), 2)
        self.assertEqual(self.builder.long_term_lack[0].work_type.code, 22)
        self.assertEqual(self.builder.long_term_lack[0].count, 1)
        self.assertEqual(self.builder.long_term_lack[0].avg_lack_day, 13.5)
        self.assertEqual(len(self.builder.long_term_lack[0].months.all()), 2)
        self.assertEqual(self.builder.long_term_lack[1].work_type.code, 14)
        self.assertEqual(self.builder.long_term_lack[1].count, 1)
        self.assertEqual(self.builder.long_term_lack[1].avg_lack_day, 8)
        self.assertEqual(len(self.builder.long_term_lack[1].months.all()), 12)

    def test_build_short_term_lack(self):
        self.builder.build_short_term_lack()
        self.assertEqual(len(self.builder.short_term_lack), 2)
        self.assertEqual(self.builder.short_term_lack[0].name, "香菇")
        self.assertEqual(self.builder.short_term_lack[0].product, None)
        self.assertEqual(self.builder.short_term_lack[0].work_type.code, 13)
        self.assertEqual(self.builder.short_term_lack[0].count, 2)
        self.assertEqual(self.builder.short_term_lack[0].avg_lack_day, 6)
        self.assertEqual(len(self.builder.short_term_lack[0].months.all()), 2)
        self.assertEqual(len(self.builder.short_term_lack), 2)
        self.assertEqual(self.builder.short_term_lack[1].name, "芒果")
        self.assertEqual(self.builder.short_term_lack[1].product, None)
        self.assertEqual(self.builder.short_term_lack[1].work_type.code, 12)
        self.assertEqual(self.builder.short_term_lack[1].count, 1)
        self.assertEqual(self.builder.short_term_lack[1].avg_lack_day, 13)
        self.assertEqual(len(self.builder.short_term_lack[1].months.all()), 2)

    def test_build_subsidy(self):
        self.builder.build_subsidy()
        self.assertEqual(self.builder.subsidy.survey.farmer_id, "670050010002")
        self.assertEqual(self.builder.subsidy.heard_app, False)
        self.assertEqual(self.builder.subsidy.none_heard_app, True)
        self.assertEqual(len(self.builder.apply), 2)
        self.assertEqual(len(self.builder.refuse), 7)
        self.assertEqual(self.builder.refuse[0].reason.name, "沒聽過")
        self.assertEqual(self.builder.refuse[1].reason.name, "無需求")
        self.assertEqual(self.builder.refuse[6].extra, "美國農業局")
