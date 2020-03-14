from . import TestCase, setup_fixtures
from apps.surveys19.models import (
    Survey,
    Population,
    LifeStyle,
    FarmerWorkDay,
    EducationLevel,
    Relationship,
    Gender,
)


class PopulationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # load fixtures
        setup_fixtures()

    def test_create_population(self):
        survey_id = Survey.objects.get(id=3)
        relationship_code = Relationship.objects.get(id=1)
        education_level_code = EducationLevel.objects.get(id=5)
        farmer_work_day = FarmerWorkDay.objects.get(id=2)
        life_style_code = LifeStyle.objects.get(id=4)
        gender_code = Gender.objects.get(id=2)

        population_list_before_size = len(Population.objects.all())

        # new value
        Population.objects.create(
            survey=survey_id,
            relationship=relationship_code,
            gender=gender_code,
            birth_year=52,
            education_level=education_level_code,
            farmer_work_day=farmer_work_day,
            life_style=life_style_code,
        )

        population_list_after_size = len(Population.objects.all())
        self.assertEquals(population_list_after_size, population_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        population_list = Population.objects.filter(survey=1)
        self.assertEquals(population_list.count(), 0)

    def test_survey_delete_all(self):
        farmer_work_day_list_before_size = len(FarmerWorkDay.objects.all())
        Survey.objects.all().delete()
        population_list = Population.objects.all()
        farmer_work_day_list_after_size = len(FarmerWorkDay.objects.all())

        self.assertEquals(len(population_list), 0)
        self.assertEquals(
            farmer_work_day_list_before_size, farmer_work_day_list_after_size
        )
