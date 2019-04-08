from django.test import TestCase
from django.core.management import call_command
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
    """
    models: LivestockMarketing, Survey
    reference models : product.yaml, loss.yaml, unit.yaml, contract.yaml
    data: livestockmarketing.yaml, survey.yaml
    main: LivestockMarketing associate other models, the one farmer has many livestock info.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "test/survey.yaml", verbosity=0)
        call_command("loaddata", "product-type.yaml", verbosity=0)
        call_command("loaddata", "product.yaml", verbosity=0)
        call_command("loaddata", "loss.yaml", verbosity=0)
        call_command("loaddata", "unit.yaml", verbosity=0)
        call_command("loaddata", "contract.yaml", verbosity=0)
        call_command("loaddata", "test/livestockmarketing.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        product_list = Product.objects.all()
        self.assertEquals(len(product_list), 297)

        loss_list = Loss.objects.all()
        self.assertEquals(len(loss_list), 8)

        unit_list = Unit.objects.all()
        self.assertEquals(len(unit_list), 15)

        contract_list = Contract.objects.all()
        self.assertEquals(len(contract_list), 4)

        livestock_marketing_list = LivestockMarketing.objects.all()
        self.assertEquals(len(livestock_marketing_list), 2)

    def test_create_livestock_marketing(self):
        survey_id = Survey.objects.get(id=3)
        product_a = Product.objects.get(id=276)
        product_b = Product.objects.get(id=268)
        loss_a = Loss.objects.get(id=8)
        unit_a = Unit.objects.get(id=13)
        contract_a = Contract.objects.get(id=2)

        livestock_marketing_list_before_size = len(LivestockMarketing.objects.all())

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

        livestock_marketing_list_after_size = len(LivestockMarketing.objects.all())
        self.assertEquals(
            livestock_marketing_list_after_size,
            livestock_marketing_list_before_size + 2,
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        livestock__marketing_list = LivestockMarketing.objects.filter(survey__id=1)
        self.assertEquals(livestock__marketing_list.count(), 0)

    def test_survey_delete_all(self):
        product_list_before_size = len(Product.objects.all())
        loss_list_before_size = len(Loss.objects.all())
        unit_list_before_size = len(Unit.objects.all())
        contract_list_before_size = len(Contract.objects.all())
        Survey.objects.all().delete()
        livestock__marketing_list = LivestockMarketing.objects.all()
        product_list_after_size = len(Product.objects.all())
        loss_list_after_size = len(Loss.objects.all())
        unit_list_after_size = len(Unit.objects.all())
        contract_list_after_size = len(Contract.objects.all())

        self.assertEquals(len(livestock__marketing_list), 0)
        self.assertEquals(product_list_before_size, product_list_after_size)
        self.assertEquals(loss_list_before_size, loss_list_after_size)
        self.assertEquals(unit_list_before_size, unit_list_after_size)
        self.assertEquals(contract_list_before_size, contract_list_after_size)
