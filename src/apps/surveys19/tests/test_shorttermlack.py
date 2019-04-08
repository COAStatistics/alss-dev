from django.test import TestCase
from django.core.management import call_command
from apps.surveys19.models import (
    Survey,
    ShortTermLack,
    WorkType,
    Month,
    Product,
    ProductType,
)


class ShortTermLackTestCase(TestCase):
    """
    models: Survey, ShortTermLack
    reference models : s19-work-type.yaml, s19-month.yaml, s19-product.yaml, s19-product-type.yaml
    data: s19-test-shorttermlack.yaml, s19-test-survey.yaml,
    main: ShortTermLack associate other models, the one farmer has many employee.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-work-type.yaml", verbosity=0)
        call_command("loaddata", "s19-month.yaml", verbosity=0)
        call_command("loaddata", "s19-product-type.yaml", verbosity=0)
        call_command("loaddata", "s19-product.yaml", verbosity=0)
        call_command("loaddata", "s19-test-shorttermlack.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        shorttermlack_list = ShortTermLack.objects.all()
        self.assertEquals(len(shorttermlack_list), 3)

    def test_create_shorttermlack(self):
        survey_id = Survey.objects.get(id=3)
        work_type_code_a = WorkType.objects.get(id=5)
        work_type_code_b = WorkType.objects.get(id=4)
        month_a = Month.objects.get(id=4)
        month_b = Month.objects.get(id=5)
        month_c = Month.objects.get(id=6)
        product = Product.objects.get(id=77)

        shorttermlack_list_before_size = len(ShortTermLack.objects.all())

        # new value
        ShortTermLack.objects.create(survey=survey_id, count=20, product=product)
        new_shorttermlack = ShortTermLack.objects.filter(survey=survey_id).last()
        new_shorttermlack.work_type = work_type_code_a
        new_shorttermlack.months.add(month_a, month_b, month_c)
        new_shorttermlack.save()

        # new value
        ShortTermLack.objects.create(survey=survey_id, count=20, product=product)
        new_shorttermlack = ShortTermLack.objects.filter(survey=survey_id).last()
        new_shorttermlack.work_type = work_type_code_b
        new_shorttermlack.months.add(month_a, month_b, month_c)
        new_shorttermlack.save()

        shorttermlack_list_after_size = len(ShortTermLack.objects.all())
        self.assertEquals(
            shorttermlack_list_after_size, shorttermlack_list_before_size + 2
        )

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        shorttermlack_list = ShortTermLack.objects.filter(survey=1)
        self.assertEquals(shorttermlack_list.count(), 0)

    def test_survey_delete_all(self):
        month_list_before_size = len(Month.objects.all())
        Survey.objects.all().delete()
        shorttermlack_list = ShortTermLack.objects.all()
        month_list_after_size = len(Month.objects.all())

        self.assertEquals(len(shorttermlack_list), 0)
        self.assertEquals(month_list_before_size, month_list_after_size)
