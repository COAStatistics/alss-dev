from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.models import Survey, LandArea, LandType, LandStatus


class ModelTestCase(TestCase):
    """
    models: LandArea, Survey
    reference models : land-type.yaml, land-status.yaml
    data: landarea.yaml, survey.yaml
    main: LandArea associate other models, the one farmer has many land types/status.
    """

    def setUp(self):
        # load fixtures
        call_command("loaddata", "test/survey.yaml", verbosity=0)
        call_command("loaddata", "land-type.yaml", verbosity=0)
        call_command("loaddata", "land-status.yaml", verbosity=0)
        call_command("loaddata", "test/landarea.yaml", verbosity=0)

    def test_loaddata(self):
        survey_list = Survey.objects.all()
        self.assertEquals(len(survey_list), 3)

        land_area_list = LandArea.objects.all()
        self.assertEquals(len(land_area_list), 2)

        land_type_list = LandType.objects.all()
        self.assertEquals(len(land_type_list), 3)

        land_status_list = LandStatus.objects.all()
        self.assertEquals(len(land_status_list), 3)

    def test_create_land_area(self):
        survey_id = Survey.objects.get(id=3)
        land_type_a = LandType.objects.get(id=2)
        land_status_a = LandStatus.objects.get(id=2)

        land_area_list_before_size = len(LandArea.objects.all())

        # new value
        LandArea.objects.create(
            survey=survey_id, type=land_type_a, status=land_status_a, value=70
        )

        land_area_list_after_size = len(LandArea.objects.all())
        self.assertEquals(land_area_list_after_size, land_area_list_before_size + 1)

    def test_survey_delete(self):
        Survey.objects.filter(id=1).delete()
        land_area_list = LandArea.objects.filter(survey__id=1)
        self.assertEquals(land_area_list.count(), 0)

    def test_survey_delete_all(self):
        land_type_list_before_size = len(LandType.objects.all())
        land_status_list_before_size = len(LandStatus.objects.all())
        Survey.objects.all().delete()
        land_area_list = LandArea.objects.all()
        land_type_list_after_size = len(LandType.objects.all())
        land_status_list_after_size = len(LandStatus.objects.all())

        self.assertEquals(len(land_area_list), 0)
        self.assertEquals(land_type_list_after_size, land_type_list_before_size)
        self.assertEquals(land_status_list_after_size, land_status_list_before_size)
