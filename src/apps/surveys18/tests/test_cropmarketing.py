from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, CropMarketing, Product, Loss, Unit, ProductType


class ModelTestCase(TestCase):
    """
    models: CropMarketing, Survey
    reference models : product.yaml, loss.yaml, unit.yaml
    data: cropmarketing.yaml, survey.yaml
    main: Cropmarketing associate other models, the one farmer has many crop info.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'product-type.yaml', verbosity=0)
        call_command('loaddata', 'product.yaml', verbosity=0)
        call_command('loaddata', 'loss.yaml', verbosity=0)
        call_command('loaddata', 'unit.yaml', verbosity=0)
        call_command('loaddata', 'test/cropmarketing.yaml', verbosity=0)


    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        crop_marketing_list = CropMarketing.objects.all()
        self.assertEquals(len(crop_marketing_list), 2)

        product_list = Product.objects.all()
        self.assertEquals(len(product_list), 297)

        loss_list = Loss.objects.all()
        self.assertEquals(len(loss_list), 8)

        unit_list = Unit.objects.all()
        self.assertEquals(len(unit_list), 15)

    def test_create_crop_marketing(self):
        survey_id = Survey.objects.get(id=3)
        product_a = Product.objects.get(id=100)
        product_b = Product.objects.get(id=150)
        loss_a = Loss.objects.get(id=1)
        unit_a = Unit.objects.get(id=5)

        crop_marketing_list_before_size = len(CropMarketing.objects.all())

        #new value
        CropMarketing.objects.create(survey=survey_id, product=product_a, loss=loss_a, unit=unit_a, land_number=0, has_facility=1)
        CropMarketing.objects.create(survey=survey_id, product=product_b)

        crop_marketing_list_after_size = len(CropMarketing.objects.all())
        self.assertEquals(crop_marketing_list_after_size, crop_marketing_list_before_size+2)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        crop_marketing_list = CropMarketing.objects.filter(survey__id=1)
        self.assertEquals(crop_marketing_list.count(), 0)

    def test_survey_delete_all(self):
        product_list_before_size = len(Product.objects.all())
        loss_list_before_size = len(Loss.objects.all())
        unit_list_before_size = len(Unit.objects.all())
        Survey.objects.all().delete()
        crop_marketing_list = CropMarketing.objects.all()
        product_list_after_size = len(Product.objects.all())
        loss_list_after_size = len(Loss.objects.all())
        unit_list_after_size = len(Unit.objects.all())

        self.assertEquals(len(crop_marketing_list), 0)
        self.assertEquals(product_list_before_size, product_list_after_size)
        self.assertEquals(loss_list_before_size, loss_list_after_size)
        self.assertEquals(unit_list_before_size, unit_list_after_size)

