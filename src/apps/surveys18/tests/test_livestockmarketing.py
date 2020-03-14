from . import TestCase, setup_fixtures
from apps.surveys18.models import (
    Survey,
    LivestockMarketing,
    Product,
    Loss,
    Unit,
    ProductType,
    Contract,
)


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_livestock_marketing(self):
        survey_id = Survey.objects.get(id=3)
        product_a = Product.objects.get(id=276)
        product_b = Product.objects.get(id=268)
        loss_a = Loss.objects.get(id=8)
        unit_a = Unit.objects.get(id=13)
        contract_a = Contract.objects.get(id=2)

        livestock_marketing_list_before_size = LivestockMarketing.objects.count()

        # new value
        LivestockMarketing.objects.create(
            survey=survey_id,
            product=product_a,
            loss=loss_a,
            unit=unit_a,
            contract=contract_a,
            raising_number=200,
        )
        LivestockMarketing.objects.create(survey=survey_id, product=product_b)

        livestock_marketing_list_after_size = LivestockMarketing.objects.count()
        self.assertEquals(
            livestock_marketing_list_after_size,
            livestock_marketing_list_before_size + 2,
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        livestock__marketing_list = LivestockMarketing.objects.filter(survey__id=1)
        self.assertEquals(livestock__marketing_list.count(), 0)

    def test_survey_delete_all(self):
        product_list_before_size = Product.objects.count()
        loss_list_before_size = Loss.objects.count()
        unit_list_before_size = Unit.objects.count()
        contract_list_before_size = Contract.objects.count()
        Survey.objects.all().delete()
        livestock__marketing_list = LivestockMarketing.objects.all()
        product_list_after_size = Product.objects.count()
        loss_list_after_size = Loss.objects.count()
        unit_list_after_size = Unit.objects.count()
        contract_list_after_size = Contract.objects.count()

        self.assertEquals(len(livestock__marketing_list), 0)
        self.assertEquals(product_list_before_size, product_list_after_size)
        self.assertEquals(loss_list_before_size, loss_list_after_size)
        self.assertEquals(unit_list_before_size, unit_list_after_size)
        self.assertEquals(contract_list_before_size, contract_list_after_size)
