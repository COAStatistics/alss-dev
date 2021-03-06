from . import TestCase, setup_fixtures
from apps.surveys18.models import (
    Survey,
    ShortTermLack,
    WorkType,
    Month,
    Product,
    ProductType,
)


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_population(self):
        survey_id = Survey.objects.get(id=3)
        work_type_code_a = WorkType.objects.get(id=4)
        month_a = Month.objects.get(id=4)
        month_b = Month.objects.get(id=5)
        month_c = Month.objects.get(id=6)
        product = Product.objects.get(id=77)

        shorttermlack_list_before_size = len(ShortTermLack.objects.all())

        # new value
        ShortTermLack.objects.create(survey=survey_id, count=20, product=product)
        new_shorttermlack = ShortTermLack.objects.get(survey=survey_id)
        new_shorttermlack.work_type = work_type_code_a
        new_shorttermlack.months.add(month_a, month_b, month_c)
        new_shorttermlack.save()

        shorttermlack_list_after_size = len(ShortTermLack.objects.all())
        self.assertEqual(
            shorttermlack_list_after_size, shorttermlack_list_before_size + 1
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        shorttermlack_list = ShortTermLack.objects.filter(survey=1)
        self.assertEqual(shorttermlack_list.count(), 0)

    def test_survey_delete_all(self):
        month_list_before_size = len(Month.objects.all())
        Survey.objects.all().delete()
        shorttermlack_list = ShortTermLack.objects.all()
        month_list_after_size = len(Month.objects.all())

        self.assertEqual(len(shorttermlack_list), 0)
        self.assertEqual(month_list_before_size, month_list_after_size)
