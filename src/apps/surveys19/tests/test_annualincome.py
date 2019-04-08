from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import Survey, AnnualIncome, MarketType, IncomeRange


class AnnualIncomeTestCase(TestCase):
    """
    models: Survey, AnnualIncome
    reference models : s19-market-type.yaml, s19-income-range.yaml
    data: s19-test-annualincome.yaml, s19-test-survey.yaml
    main: AnnualIncome associate other models, the one farmer has many market-type/income-range.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-market-type.yaml", verbosity=0)
        call_command("loaddata", "s19-income-range.yaml", verbosity=0)
        call_command("loaddata", "s19-test-annualincome.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        annual_income_list = AnnualIncome.objects.all()
        self.assertEquals(len(annual_income_list), 2)

        market_type_list = MarketType.objects.all()
        self.assertEquals(len(market_type_list), 5)

        income_range_list = IncomeRange.objects.all()
        self.assertEquals(len(income_range_list), 11)

    def test_create_annual_income(self):
        survey_id = Survey.objects.get(id=3)
        market_type_a = MarketType.objects.get(id=2)
        income_range_a = IncomeRange.objects.get(id=8)
        market_type_b = MarketType.objects.get(id=3)
        income_range_b = IncomeRange.objects.get(id=1)
        market_type_c = MarketType.objects.get(id=5)
        income_range_c = IncomeRange.objects.get(id=8)

        annual_income_list_before_size = len(AnnualIncome.objects.all())

        # new value
        AnnualIncome.objects.create(
            survey=survey_id, market_type=market_type_a, income_range=income_range_a
        )
        AnnualIncome.objects.create(
            survey=survey_id, market_type=market_type_b, income_range=income_range_b
        )
        AnnualIncome.objects.create(
            survey=survey_id, market_type=market_type_c, income_range=income_range_c
        )

        annual_income_list_after_size = len(AnnualIncome.objects.all())
        self.assertEquals(
            annual_income_list_after_size, annual_income_list_before_size + 3
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        annual_income_list = AnnualIncome.objects.filter(survey__id=1)
        self.assertEquals(annual_income_list.count(), 0)

    def test_survey_delete_all(self):
        market_type_list_before_size = len(MarketType.objects.all())
        income_range_list_before_size = len(IncomeRange.objects.all())
        Survey.objects.all().delete()
        annual_income_list = AnnualIncome.objects.all()
        market_type_list_after_size = len(MarketType.objects.all())
        income_range_list_after_size = len(IncomeRange.objects.all())

        self.assertEquals(len(annual_income_list), 0)
        self.assertEquals(market_type_list_after_size, market_type_list_before_size)
        self.assertEquals(income_range_list_after_size, income_range_list_before_size)
