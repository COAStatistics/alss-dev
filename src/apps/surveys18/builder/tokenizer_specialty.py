from .exceptions import SignError, CreateModelError

from apps.surveys18.models import (
    Survey,
    AddressMatch,
    FarmRelatedBusiness,
    Business,
    ManagementType,
    Phone,
    LandArea,
    LandType,
    LandStatus,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    LivestockMarketing,
    Population,
    EducationLevel,
    FarmerWorkDay,
    Gender,
    Relationship,
)


class Builder(object):
    def __init__(self, string):
        self.survey = None
        self.phones = []
        self.address = None
        self.land_area = []
        self.business = []
        self.crop_marketing = []
        self.livestock_marketing = []
        self.population = []

        self.string = [
            x.replace(u"\u3000", u"").replace(" ", "").strip()
            for x in string.split(",")
        ]

        if len(self.string) != 58:
            raise SignError(",")

    def build(self, readonly=True):
        self.build_survey(readonly=readonly)
        try:
            self.build_phone()
            self.build_address()
            self.build_land_area()
            self.build_business()
            self.build_management()
            self.build_crop_marketing()
            self.build_livestock_marketing()
            self.build_population()
        except Exception:
            Survey.objects.filter(
                farmer_id=self.survey.farmer_id, readonly=self.survey.readonly
            ).delete()
            raise

    @staticmethod
    def data_exit(string):
        if string:
            return string
        else:
            return None

    def build_survey(self, readonly=True):
        farmer_id = self.string[2]
        total_pages = 1
        page = 1
        name = self.string[7]
        is_updated = True
        obj = Survey.objects.filter(farmer_id=farmer_id, readonly=readonly).first()
        if obj:
            self.survey = obj
        else:
            try:
                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    farmer_name=name,
                    page=page,
                    total_pages=total_pages,
                    is_updated=is_updated,
                    readonly=readonly,
                )

            except ValueError:
                raise CreateModelError("Survey")
            else:
                self.survey = survey

    def build_phone(self):
        phones = self.string[8:10]
        if len(phones[0]) > 0 or len(phones[1]) > 0:
            try:
                for number in phones:
                    if len(number) > 0:
                        phone = Phone.objects.create(survey=self.survey, phone=number)
                        self.phones.append(phone)
            except ValueError:
                raise CreateModelError("Phone")

    def build_address(self):
        address = self.string[10:12]
        obj = Business.objects.filter(survey=self.survey).first()
        if obj is None:
            if len(address[0]) > 0:
                try:
                    if address[0] == "是":
                        mismatch = False
                        match = True
                    else:
                        mismatch = True
                        match = False

                    address = AddressMatch.objects.create(
                        survey=self.survey,
                        match=match,
                        mismatch=mismatch,
                        address=address[1],
                    )
                except ValueError:
                    raise CreateModelError("Address Match")
                else:
                    self.address = address

    def build_land_area(self):
        land_area_str = self.string[13:19]
        # print(land_area_str)
        if len(land_area_str[0]) > 0:
            try:
                for i in range(0, len(land_area_str), 3):
                    for j in range(1, 4):
                        if land_area_str[i + j - 1]:
                            if int(land_area_str[i + j - 1]) > 0:
                                type_id = 1 if i < 3 else 2
                                status = j

                                land_type = LandType.objects.get(id=type_id)
                                land_status = LandStatus.objects.get(id=status)

                                land_area = LandArea.objects.create(
                                    survey=self.survey,
                                    type=land_type,
                                    status=land_status,
                                    value=int(land_area_str[i + j - 1]),
                                )
                                self.land_area.append(land_area)

                if land_area_str[-1]:
                    if int(land_area_str[-1]) > 0:
                        land_type = LandType.objects.get(id=3)
                        land_area = LandArea.objects.create(
                            survey=self.survey, type=land_type
                        )
                        self.land_area.append(land_area)

            except ValueError:
                raise CreateModelError("Land Area")

    def build_business(self):
        business_str = self.string[41:51]
        if len(business_str) > 1:
            try:
                if business_str[0] == "0":
                    business = Business.objects.create(
                        survey=self.survey,
                        farm_related_business=FarmRelatedBusiness.objects.get(code=1),
                    )
                    self.business.append(business)
                for i in range(1, 8):
                    if business_str[i] == "1":
                        num = i + 1
                        business = Business.objects.create(
                            survey=self.survey,
                            farm_related_business=FarmRelatedBusiness.objects.get(
                                code=num
                            ),
                        )
                        self.business.append(business)
                if business_str[8] == "1":
                    business = Business.objects.create(
                        survey=self.survey,
                        farm_related_business=FarmRelatedBusiness.objects.get(code=9),
                        extra=business_str[9],
                    )
                    self.business.append(business)
                elif len(business_str[9]) > 0:
                    business = Business.objects.create(
                        survey=self.survey, extra=business_str[9]
                    )
                    self.business.append(business)

            except ValueError:
                raise CreateModelError("Business")

    def build_management(self):
        management_str = self.string[57]
        if len(management_str) > 0:
            try:
                char = management_str.split(".")
                num = int(char[0])
                if num < 3:
                    num = num
                elif (num > 3) and (num < 8):
                    num = num + 1
                elif num == 10:
                    num = 12
                elif num == 12:
                    num = 13
                elif (num == 11) or (num == 13) or (num == 14) or (num == 15):
                    num = 14
                else:
                    num = 0

                if num > 0:
                    management_type = ManagementType.objects.get(code=num)
                    self.survey.management_types.add(management_type)

            except ValueError:
                raise CreateModelError("management")

    def build_crop_marketing(self):
        crop_marketing_str = self.string[20:31]
        if len(crop_marketing_str[0]) > 0:
            try:
                product_str = crop_marketing_str[0]
                product = Product.objects.filter(code=product_str).first()
                land_number = crop_marketing_str[2]
                land_area = crop_marketing_str[3]
                plant_times = crop_marketing_str[4]
                unit_str = int(crop_marketing_str[5]) if crop_marketing_str[5] else None
                unit = Unit.objects.filter(code=unit_str, type=1).first()
                total_yield = crop_marketing_str[6]
                unit_price = crop_marketing_str[7]
                has_facility_str = int(crop_marketing_str[8])
                if has_facility_str == 2:
                    has_facility = 0
                elif has_facility_str == 1:
                    has_facility = 1
                else:
                    has_facility = None

                loss_str = (
                    int(crop_marketing_str[10]) if crop_marketing_str[10] else None
                )
                loss = Loss.objects.filter(code=loss_str, type=1).first()
                # print(product,land_number,land_number,plant_times,unit,total_yield,unit_price,has_facility,loss)

                crop_marketing = CropMarketing.objects.create(
                    survey=self.survey,
                    product=product,
                    land_number=land_number,
                    land_area=land_area,
                    plant_times=plant_times,
                    unit=unit,
                    total_yield=total_yield,
                    unit_price=unit_price,
                    has_facility=has_facility,
                    loss=loss,
                )
                self.crop_marketing.append(crop_marketing)

            except ValueError:
                raise CreateModelError("CropMarketing")

    def build_livestock_marketing(self):
        livestock_str = self.string[32:42]
        if len(livestock_str[0]) > 0:
            try:
                product_str = livestock_str[0]
                product = Product.objects.filter(code=product_str).first()
                unit_str = livestock_str[2]
                unit = Unit.objects.filter(code=unit_str, type=2).first()
                raising_number = int(livestock_str[3]) if livestock_str[3] else None
                total_yield = int(livestock_str[4]) if livestock_str[4] else None
                unit_price = int(livestock_str[5]) if livestock_str[5] else None
                contract_str = int(livestock_str[6]) if livestock_str[6] else None
                contract = Contract.objects.filter(code=contract_str).first()
                loss_str = int(livestock_str[8]) if livestock_str[8] else None
                loss = Loss.objects.filter(code=loss_str, type=2).first()

                # print(product,unit,raising_number,total_yield,unit_price,contract,loss)

                livestock_marketing = LivestockMarketing.objects.create(
                    survey=self.survey,
                    product=product,
                    unit=unit,
                    raising_number=raising_number,
                    total_yield=total_yield,
                    unit_price=unit_price,
                    contract=contract,
                    loss=loss,
                )
                self.livestock_marketing.append(livestock_marketing)
            except ValueError:
                raise CreateModelError("LivestockMarketing")

    def build_population(self):
        population_str = self.string[52:57]
        if len(population_str[0]) > 0:
            try:
                relationship_str = int(population_str[0]) if population_str[0] else None
                relationship = Relationship.objects.filter(
                    code=relationship_str
                ).first()
                gender_str = int(population_str[1]) if population_str[1] else None
                gender = Gender.objects.filter(code=gender_str).first()

                birth_year = (
                    int(int(population_str[2]) / 100) if population_str[2] else None
                )

                education_level_str = (
                    int(population_str[3]) if population_str[3] else None
                )
                education_level = EducationLevel.objects.filter(
                    code=education_level_str
                ).first()
                farmer_work_day_str = (
                    int(population_str[4]) if population_str[4] else None
                )

                if farmer_work_day_str:
                    if farmer_work_day_str == 8:
                        farmer_work_day_id = 1
                    else:
                        farmer_work_day_id = farmer_work_day_str + 1
                farmer_work_day = FarmerWorkDay.objects.filter(
                    code=farmer_work_day_id
                ).first()

                if birth_year < 92:
                    population = Population.objects.create(
                        survey=self.survey,
                        relationship=relationship,
                        gender=gender,
                        birth_year=birth_year,
                        education_level=education_level,
                        farmer_work_day=farmer_work_day,
                    )
                    self.population.append(population)

            except ValueError:
                raise CreateModelError("Population")
