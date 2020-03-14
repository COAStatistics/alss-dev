from . import TestCase, setup_fixtures
from apps.surveys19.models import (
    Survey,
    CropMarketing,
    Product,
    Loss,
    Unit,
)


class CropMarketingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_crop_marketing(self):
        survey_id = Survey.objects.get(id=3)
        product_a = Product.objects.get(id=100)
        product_b = Product.objects.get(id=150)
        loss_a = Loss.objects.get(id=1)
        unit_a = Unit.objects.get(id=5)

        crop_marketing_list_before_size = len(CropMarketing.objects.all())

        # new value
        CropMarketing.objects.create(
            survey=survey_id,
            product=product_a,
            loss=loss_a,
            unit=unit_a,
            land_number=0,
            has_facility=1,
        )
        CropMarketing.objects.create(survey=survey_id, product=product_b)

        crop_marketing_list_after_size = len(CropMarketing.objects.all())
        self.assertEquals(
            crop_marketing_list_after_size, crop_marketing_list_before_size + 2
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        crop_marketing_list = CropMarketing.objects.filter(survey__id=1)
        self.assertEquals(crop_marketing_list.count(), 0)

    def test_survey_delete_all(self):
        product_list_before_size = Product.objects.count()
        loss_list_before_size = Loss.objects.count()
        unit_list_before_size = Unit.objects.count()
        Survey.objects.all().delete()
        crop_marketing_list = CropMarketing.objects.all()
        product_list_after_size = Product.objects.count()
        loss_list_after_size = Loss.objects.count()
        unit_list_after_size = Unit.objects.count()

        self.assertEquals(len(crop_marketing_list), 0)
        self.assertEquals(product_list_before_size, product_list_after_size)
        self.assertEquals(loss_list_before_size, loss_list_after_size)
        self.assertEquals(unit_list_before_size, unit_list_after_size)
