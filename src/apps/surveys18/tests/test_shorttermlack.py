from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, ShortTermLack, WorkType, Month, Product, ProductType

class ModelTestCase(TestCase):
    """
    models: Survey, ShortTermLack
    reference models : WorkType, Month, Product
    data: shorttermlack.yaml, survey.yaml, work-type.yaml, month.yaml, product.yaml, product-type.yaml
    main: ShortTermLack associate other models, the one farmer has many employee.
    """

    def setUp(self):
        # load fixtures
        call_command('loaddata', 'test/survey.yaml', verbosity=0)
        call_command('loaddata', 'work-type.yaml', verbosity=0)
        call_command('loaddata', 'month.yaml', verbosity=0)
        call_command('loaddata', 'product-type.yaml', verbosity=0)
        call_command('loaddata', 'product.yaml', verbosity=0)
        call_command('loaddata', 'test/shorttermlack.yaml', verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        shorttermlack_list = ShortTermLack.objects.all()
        self.assertEquals(len(shorttermlack_list), 3)

    def test_create_population(self):
        survey_id = Survey.objects.get(id=3)
        work_type_code_a = WorkType.objects.get(id=5)
        work_type_code_b = WorkType.objects.get(id=4)
        month_a = Month.objects.get(id=4)
        month_b = Month.objects.get(id=5)
        month_c = Month.objects.get(id=6)
        product = Product.objects.get(id=77)

        shorttermlack_list_before_size = len(ShortTermLack.objects.all())

        #new value
        ShortTermLack.objects.create(survey=survey_id, count=20, product=product)
        new_shorttermlack = ShortTermLack.objects.get(survey=survey_id)
        new_shorttermlack.work_types.add(work_type_code_a, work_type_code_b)
        new_shorttermlack.months.add(month_a, month_b, month_c)
        new_shorttermlack.save()

        shorttermlack_list_after_size = len(ShortTermLack.objects.all())
        self.assertEquals(shorttermlack_list_after_size, shorttermlack_list_before_size+1)

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
