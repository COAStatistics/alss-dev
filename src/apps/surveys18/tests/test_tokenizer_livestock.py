from django.test import TestCase
from django.core.management import call_command
from apps.surveys18.builder.tokenizer_specialty import Builder
from apps.surveys18.models import Survey, LivestockMarketing


class ModelTestCase(TestCase):
    def setUp(self):
        call_command("loaddata", "land-status.yaml", verbosity=0)
        call_command("loaddata", "farm-related-business.yaml", verbosity=0)
        call_command("loaddata", "management-type.yaml", verbosity=0)
        call_command("loaddata", "product-type.yaml", verbosity=0)
        call_command("loaddata", "product.yaml", verbosity=0)
        call_command("loaddata", "loss.yaml", verbosity=0)
        call_command("loaddata", "unit.yaml", verbosity=0)
        call_command("loaddata", "land-type.yaml", verbosity=0)
        call_command("loaddata", "contract.yaml", verbosity=0)
        call_command("loaddata", "age-scope.yaml", verbosity=0)
        call_command("loaddata", "gender.yaml", verbosity=0)
        call_command("loaddata", "relationship.yaml", verbosity=0)
        call_command("loaddata", "education-level.yaml", verbosity=0)
        call_command("loaddata", "farmer-work-day.yaml", verbosity=0)
        call_command("loaddata", "life-style.yaml", verbosity=0)
        call_command("loaddata", "other-farm-work.yaml", verbosity=0)

        lst = [
            "1344,106,640240014040,1,39,,7,蘇受貞　　,0912798577 ,07-6978832 ,否,高雄市路竹區社東里東安路36巷43號,,0,0,0,0,0,0,,,,,,,,,,,,,1,G008,中雞(請填品項，如白肉雞/有色肉雞/蛋雞),4,48200,96500,100,0,,0,1,0,0,0,0,0,1,0,0,自行載送販賣,1,1,2,04900 ,6,7,12. 雞",
            "1344,106,640240014040,2,39,,,,,,,,,,,,,,,,,,,,,,,,,,,2,G001,蛋雞,4,3200,0,0,0,烏骨雞,0,,,,,,,,,,,2,2,1,04800 ,5,2,",
            "1344,106,640240014040,3,39,,,,,,,,,,,,,,,,,,,,,,,,,,,3,G001,蛋雞,4,3800,0,0,0,土雞種,0,,,,,,,,,,,3,3,1,07200 ,8,7,",
            "1344,106,640240014040,4,39,,,,,,,,,,,,,,,,,,,,,,,,,,,4,G001,蛋雞,4,11000,0,0,0,紅皮蛋雞,0,,,,,,,,,,,4,3,1,07700 ,8,7,",
            "1344,106,640240014040,5,39,,,,,,,,,,,,,,,,,,,,,,,,,,,5,G001,蛋雞,4,14500,0,0,0,白蛋雞,0,,,,,,,,,,,5,8,2,07200 ,8,7,",
            "1344,106,640240014040,6,39,,,,,,,,,,,,,,,,,,,,,,,,,,,6,G006,淘汰雞,4,0,24500,12,0,,0,,,,,,,,,,,6,8,2,07700 ,8,7,",
            "1344,106,640240014040,7,39,,,,,,,,,,,,,,,,,,,,,,,,,,,7,G010,雞蛋,2,0,585,1200,0,,0,,,,,,,,,,,7,4,2,10500 ,1,8,",
            "1344,106,640240014040,99,39,,,,,,,,,,,,,,,,,,,,,,,,,,,8,G010,雞蛋,2,0,1050,840,0,,0,,,,,,,,,,,,,,,,,",
            "1344,106,640240014040,,39,,,,,,,,,,,,,,,,,,,,,,,,,,,9,G010,雞蛋,2,0,3360,660,0,,0,,,,,,,,,,,,,,,,,",
            "1344,106,640240014040,,39,,,,,,,,,,,,,,,,,,,,,,,,,,,10,G010,雞蛋,2,0,5750,540,0,,0,,,,,,,,,,,,,,,,,",
        ]

        for string in lst:
            self.builder = Builder(string)
            self.builder.build()

    def test_build_livestock_marketing(self):
        survey = Survey.objects.filter(farmer_id="640240014040").first()
        print("=================")

        self.assertEquals(survey.livestock_marketings.all().count(), 10)
