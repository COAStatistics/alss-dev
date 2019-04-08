from django.test import TestCase
from django.core.management import call_command
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
    """
    models: Population, Survey
    reference models : s19-life-style.yaml, s19-farmer-work-day.yaml,
                       s19-education-level.yaml, s19-relationship.yaml, s19-gender.yaml
    data: s19-test-population.yaml, s19-test-survey.yaml,
    main: Population associate other models, the one farmer has many population.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "s19-test-survey.yaml", verbosity=0)
        call_command("loaddata", "s19-education-level.yaml", verbosity=0)
        call_command("loaddata", "s19-farmer-work-day.yaml", verbosity=0)
        call_command("loaddata", "s19-life-style.yaml", verbosity=0)
        call_command("loaddata", "s19-relationship.yaml", verbosity=0)
        call_command("loaddata", "s19-gender.yaml", verbosity=0)
        call_command("loaddata", "s19-test-population.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        population_list = Population.objects.all()
        self.assertEquals(len(population_list), 4)

        educationlevel_list = EducationLevel.objects.all()
        self.assertEquals(len(educationlevel_list), 5)

        farmerworkday_list = FarmerWorkDay.objects.all()
        self.assertEquals(len(farmerworkday_list), 8)

        lifestyle_list = LifeStyle.objects.all()
        self.assertEquals(len(lifestyle_list), 8)

        relationship_list = Relationship.objects.all()
        self.assertEquals(len(relationship_list), 8)

        gender_list = Gender.objects.all()
        self.assertEquals(len(gender_list), 2)

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
