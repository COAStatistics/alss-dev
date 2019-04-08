from .exceptions import SignError, StringLengthError, CreateModelError
from django.contrib.contenttypes.models import ContentType

from apps.surveys18.models import (
    MarketType,
    IncomeRange,
    AnnualIncome,
    Survey,
    AddressMatch,
    FarmRelatedBusiness,
    Business,
    ManagementType,
    Lack,
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
    Facility,
    PopulationAge,
    Population,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
    OtherFarmWork,
    Subsidy,
    RefuseReason,
    AgeScope,
    LongTermHire,
    ShortTermHire,
    WorkType,
    NumberWorkers,
    NoSalaryHire,
    ShortTermLack,
    LongTermLack,
    Gender,
    ProductType,
    Relationship,
    Month,
    Refuse,
)


class Builder(object):
    def __init__(self, string):
        token_size, self.more_page = self.check_string(string)
        delimiter_plus = "+"
        delimiter_pound = "#+"
        cut_token = []

        if self.more_page:
            for t in string.split(delimiter_plus):
                cut_token.append(t)
        else:
            tokens = string.split(delimiter_pound)
            for token in tokens:
                for t in token.split(delimiter_plus):
                    cut_token.append(t)

        self.string = cut_token

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
            self.build_annual_income()
            self.build_population_age()
            self.build_population()
            self.build_hire()
            self.build_long_term_hire()
            self.build_short_term_hire()
            self.build_no_salary_hire()
            self.build_long_term_lack()
            self.build_short_term_lack()
            self.build_lack()
            self.build_subsidy()
        except Exception as e:
            Survey.objects.filter(
                farmer_id=self.survey.farmer_id,
                page=self.survey.page,
                readonly=self.survey.readonly,
            ).delete()
            raise e

    @staticmethod
    def check_string(string):
        delimiter_plus = "+"
        delimiter_pound = "#+"
        slices_cnt = string.count(delimiter_plus)
        slices_pound_cnt = string.count(delimiter_pound)
        slices = string.split(delimiter_plus)
        slices_pound = string.split(delimiter_pound)

        if slices_cnt != 11:
            if slices_cnt != 11:
                raise SignError(sign="+")
        else:
            if len(slices[0]) == 16:
                return True, True
            else:
                if slices_pound_cnt != 2:
                    raise SignError(sign="#+")
                elif (
                    (slices_pound[1].find("#") is -1)
                    or (slices_pound[-1].find("#") is -1)
                    or (slices_pound[-2].find("#") is -1)
                ):
                    raise SignError(sign="#")
        return True, False

    @staticmethod
    def id_and_value(string):
        cnt = 0
        id = 0
        for i in range(0, len(string)):
            if string[i] == "1":
                id = i + 1
                cnt = cnt + 1
        return cnt, id

    def build_survey(self, readonly=True):
        try:
            string = self.string[0]
            farmer_id = string[0:12]
            total_pages = int(string[12:14])
            page = int(string[14:16])
            if len(self.string[0]) > 16:
                self.more_page = False
                name = string[16:23].replace("#", "")
                ori_class = int(string[44:46])
                string = self.string[-1]
                note = string.split("#")[0]
                period_h = int(string.split("#")[1][-9:-6])
                period_m = int(string.split("#")[1][-6:-4])
                distance_km = int(string.split("#")[1][-4:])

        except ValueError as e:
            raise StringLengthError(target="Survey", msg=e)

        # dup
        obj = Survey.objects.filter(
            page=page, farmer_id=farmer_id, readonly=readonly, is_updated=False
        ).all()
        obj_2 = Survey.objects.filter(
            page=page, farmer_id=farmer_id, readonly=False, is_updated=False
        ).all()
        obj_3 = Survey.objects.filter(
            page=page, farmer_id=farmer_id, readonly=readonly, is_updated=True
        ).all()
        if obj:
            obj.delete()
        if obj_2:
            obj_2.delete()
        if obj_3:
            self.survey = obj_3
        try:
            if obj_3:
                self.survey.farmer_name = name
                self.survey.total_pages = total_pages
                self.survey.note = note
                self.survey.period = period_h * 60 + period_m
                self.survey.distance = distance_km
                self.survey.save()

            elif self.more_page:
                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    page=page,
                    total_pages=total_pages,
                    readonly=readonly,
                    is_updated=False,
                )
            else:
                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    page=page,
                    total_pages=total_pages,
                    farmer_name=name,
                    origin_class=ori_class,
                    readonly=readonly,
                    is_updated=False,
                    note=note,
                    period=period_h * 60 + period_m,
                    distance=distance_km,
                )
        except ValueError as e:
            raise CreateModelError(target="Survey", msg=e)

        else:
            self.survey = survey

    def build_phone(self):
        if self.survey.is_updated is False:
            if self.more_page is False:
                try:
                    string = self.string[0]
                    phones = string[23:44].replace("#", "").split("/")
                except ValueError as e:
                    raise StringLengthError(target="Phone", msg=e)
                else:
                    try:
                        self.phones = []
                        for number in phones:
                            if len(number) > 0:
                                phone = Phone.objects.create(
                                    survey=self.survey, phone=number
                                )
                                self.phones.append(phone)
                    except ValueError as e:
                        raise CreateModelError(target="Phone", msg=e)

    def build_address(self):
        if self.survey.is_updated is False:
            match = False
            mismatch = False
            if self.more_page is False:
                try:
                    string = self.string[0]
                    match_str = string[46:47]
                    mismatch_str = string[47:48]
                    address = string[48:]
                    if match_str == "1":
                        match = True
                    if mismatch_str == "1":
                        mismatch = True
                except ValueError as e:
                    raise StringLengthError(target="Address Match", msg=e)
                else:
                    try:
                        address = AddressMatch.objects.create(
                            survey=self.survey,
                            match=match,
                            mismatch=mismatch,
                            address=address,
                        )
                    except ValueError as e:
                        raise CreateModelError(target="Address Match", msg=e)
                    else:
                        self.address = address

    def build_land_area(self):
        if self.survey.is_updated is False:
            if self.more_page is False:
                try:
                    string = self.string[1]
                    area_str = string[0:26]
                except ValueError as e:
                    raise StringLengthError(target="Land Area", msg=e)
                else:
                    try:
                        self.land_area = []
                        cnt = 0
                        for i in range(5, len(area_str), 5):
                            if int(area_str[cnt * 5 : i]) > 0:

                                type = 1 if cnt < 3 else 2
                                status = int((i / 5)) - 3 if i / 5 > 3 else int((i / 5))

                                land_type = LandType.objects.get(id=type)
                                land_status = LandStatus.objects.get(id=status)

                                land_area = LandArea.objects.create(
                                    survey=self.survey,
                                    type=land_type,
                                    status=land_status,
                                    value=int(area_str[cnt * 5 : i]),
                                )
                                self.land_area.append(land_area)
                            cnt = cnt + 1

                        if area_str[-1] == "1":
                            land_type = LandType.objects.get(id=3)
                            land_area = LandArea.objects.create(
                                survey=self.survey, type=land_type
                            )
                            self.land_area.append(land_area)

                    except ValueError as e:
                        raise CreateModelError(target="Land Area", msg=e)

    def build_business(self):
        if self.survey.is_updated is False:
            if self.more_page is False:
                try:
                    string = self.string[1]
                    business_str = string[26:].split("#")[0]

                except ValueError as e:
                    raise StringLengthError(target="Business", msg=e)
                else:
                    try:
                        self.business = []
                        for i in range(0, 8):
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
                                farm_related_business=FarmRelatedBusiness.objects.get(
                                    code=9
                                ),
                                extra=business_str[9:],
                            )
                            self.business.append(business)
                        elif len(business_str[8:]) > 2:
                            business = Business.objects.create(
                                survey=self.survey, extra=business_str[9:]
                            )
                            self.business.append(business)

                    except ValueError as e:
                        raise CreateModelError(target="Business", msg=e)

    def build_management(self):
        if self.survey.is_updated is False:
            if self.more_page is False:
                try:
                    string = self.string[1]
                    management_str = string[26:].split("#")[1]
                    if len(management_str) != 14:
                        raise StringLengthError(target="management")
                except ValueError as e:
                    raise StringLengthError(target="management", msg=e)
                else:
                    try:
                        for i in range(0, 14):
                            if management_str[i] == "1":
                                num = i + 1
                                management_type = ManagementType.objects.get(id=num)
                                self.survey.management_types.add(management_type)
                    except ValueError as e:
                        raise CreateModelError(target="management", msg=e)

    def build_crop_marketing(self):
        if self.survey.is_updated is False:
            string = self.string[2]
            if len(string) % 25 != 0:
                raise StringLengthError(target="CropMarketing")
            else:
                if len(string) > 0:
                    try:
                        self.crop_marketing = []
                        num = int(len(string) / 25)
                        for i in range(0, num):
                            crop_marketing = string[i * 25 : i * 25 + 25]
                            product_str = crop_marketing[0:4]
                            product = Product.objects.filter(code=product_str).first()
                            land_number = int(crop_marketing[4:5])
                            land_area = int(crop_marketing[5:9])
                            plant_times = int(crop_marketing[9:10])
                            unit_str = int(crop_marketing[10:11])
                            unit = Unit.objects.filter(code=unit_str, type=1).first()
                            total_yield = int(crop_marketing[11:18])
                            unit_price = int(crop_marketing[18:23])
                            has_facility_str = int(crop_marketing[23:24])
                            if has_facility_str == 0:
                                has_facility = None
                            elif has_facility_str == 1:
                                has_facility = 1
                            else:
                                has_facility = 0
                            loss_str = int(crop_marketing[24:25])
                            loss = Loss.objects.filter(code=loss_str, type=1).first()

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
                    except ValueError as e:
                        raise CreateModelError(target="CropMarketing", msg=e)

    def build_livestock_marketing(self):
        if self.survey.is_updated is False:
            string = self.string[3]
            if self.more_page is False:
                livestock_str = string[:-22]
            else:
                livestock_str = string

            if (len(livestock_str)) % 24 != 0:
                raise StringLengthError(target="LivestockMarketing")
            else:
                if len(string) > 0:
                    try:
                        self.livestock_marketing = []
                        num = int(len(livestock_str) / 24)
                        for i in range(0, num):
                            livestock = livestock_str[i * 24 : i * 24 + 24]
                            product_str = livestock[0:4]
                            product = Product.objects.filter(code=product_str).first()
                            unit_str = int(livestock[4:5])
                            unit = Unit.objects.filter(code=unit_str, type=2).first()
                            raising_number = int(livestock[5:11])
                            total_yield = int(livestock[11:17])
                            unit_price = int(livestock[17:22])
                            contract_str = int(livestock[22:23])
                            contract = Contract.objects.filter(
                                code=contract_str
                            ).first()
                            loss_str = int(livestock[23:24])
                            loss = Loss.objects.filter(code=loss_str, type=2).first()

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
                    except ValueError as e:
                        raise CreateModelError(target="LivestockMarketing", msg=e)

    def build_annual_income(self):
        if self.more_page is False:
            string = self.string[3]
            annual_income_str = string[-22:]
            if len(annual_income_str) != 22:
                raise StringLengthError(target="AnnualIncome")
            else:
                try:
                    self.annual_income = []
                    for i in range(0, 10, 2):
                        value = int(annual_income_str[i : i + 2])
                        if value > 0:
                            num = i / 2 + 1
                            market_type = MarketType.objects.get(id=num)
                            income_range = IncomeRange.objects.get(id=value)
                            annual_income = AnnualIncome.objects.create(
                                survey=self.survey,
                                market_type=market_type,
                                income_range=income_range,
                            )
                            self.annual_income.append(annual_income)

                except ValueError as e:
                    raise CreateModelError(target="AnnualIncome", msg=e)

    def build_population_age(self):
        if self.more_page is False:
            string = self.string[3]
            population_age_str = string[-12:]
            if len(population_age_str) != 12:
                raise StringLengthError(target="PopulationAge")
            else:
                try:
                    self.population_age = []
                    for j in range(0, len(population_age_str), 6):
                        for i in range(0, 6, 2):

                            value = int(population_age_str[i + j : i + j + 2])
                            age_scope = AgeScope.objects.get(id=int(j / 4 + 4))
                            if i / 2 == 1 and value > 0:
                                gender = Gender.objects.get(id=1)
                                population_age = PopulationAge.objects.create(
                                    survey=self.survey,
                                    gender=gender,
                                    age_scope=age_scope,
                                    count=value,
                                )
                                self.population_age.append(population_age)
                            elif i / 2 == 2 and value > 0:
                                gender = Gender.objects.get(id=2)
                                population_age = PopulationAge.objects.create(
                                    survey=self.survey,
                                    gender=gender,
                                    age_scope=age_scope,
                                    count=value,
                                )
                                self.population_age.append(population_age)

                except ValueError as e:
                    raise CreateModelError(target="PopulationAge", msg=e)

    def build_population(self):
        string = self.string[4]
        if self.more_page is False:
            string = string[:-2]

        if (len(string)) % 29 != 0:
            raise StringLengthError(target="Population")
        else:
            if len(string) > 0:
                try:
                    self.population = []

                    for i in range(0, len(string), 29):
                        population_str = string[i : i + 29]
                        relationship_str = int(population_str[2:4])

                        relationship = Relationship.objects.filter(
                            code=relationship_str
                        ).first()
                        gender_str = int(population_str[4:5])
                        gender = Gender.objects.filter(code=gender_str).first()

                        birth_year = int(population_str[5:8])
                        education_level_str = int(population_str[8:10])
                        education_level = EducationLevel.objects.filter(
                            code=education_level_str
                        ).first()
                        farmer_work_day_str = population_str[10:18]
                        farmer_work_day_cnt, farmer_work_day_id = self.id_and_value(
                            farmer_work_day_str
                        )
                        if farmer_work_day_cnt != 1:
                            farmer_work_day = None
                        else:
                            farmer_work_day = FarmerWorkDay.objects.filter(
                                code=farmer_work_day_id
                            ).first()

                        life_style_str = population_str[18:26]
                        life_style_cnt, life_style_id = self.id_and_value(
                            life_style_str
                        )
                        if farmer_work_day_cnt != 1:
                            life_style = None
                        else:
                            life_style = LifeStyle.objects.filter(
                                code=life_style_id
                            ).first()

                        other_farm_work_str = population_str[26:]
                        other_farm_work_cnt, other_farm_work_id = self.id_and_value(
                            other_farm_work_str
                        )
                        if other_farm_work_cnt != 1:
                            other_farm_work = None
                        else:

                            other_farm_work = OtherFarmWork.objects.filter(
                                id=other_farm_work_id
                            ).first()

                        # print(relationship_str, gender_str, birth_year, education_level_str, farmer_work_day_str, life_style_str,
                        #       other_farm_work_str)
                        # print(relationship,gender,birth_year,education_level,farmer_work_day,life_style,other_farm_work)

                        if self.survey.is_updated:
                            obj = Population.objects.get(
                                survey__id=self.survey.id,
                                birth_year=birth_year,
                                gender=gender,
                                relationship=relationship,
                            )

                            if obj:
                                obj.life_style = life_style
                                obj.other_farm_work = other_farm_work
                                obj.save()
                        else:
                            population = Population.objects.create(
                                survey=self.survey,
                                relationship=relationship,
                                gender=gender,
                                birth_year=birth_year,
                                education_level=education_level,
                                farmer_work_day=farmer_work_day,
                                life_style=life_style,
                                other_farm_work=other_farm_work,
                            )
                            self.population.append(population)

                except ValueError as e:
                    raise CreateModelError(target="Population", msg=e)

    def build_hire(self):
        if self.more_page is False:
            string = self.string[4][-2:]
            try:
                if string[0] == "1":
                    self.survey.non_hire = True
                else:
                    self.survey.non_hire = False

                if string[1] == "1":
                    self.survey.hire = True
                else:
                    self.survey.hire = False

                self.survey.save()

                print(self.survey.non_hire)
                print(self.survey.hire)

            except ValueError as e:
                raise CreateModelError(target="hire", msg=e)

    def build_long_term_hire(self):
        string = self.string[5]
        if len(string) % 30 != 0:
            raise StringLengthError("LongTermHire")
        else:
            if len(string) > 0:
                try:
                    self.long_term_hire = []
                    for i in range(0, len(string), 30):
                        long_term_hire_str = string[i : i + 30]
                        work_type_str = int(long_term_hire_str[0:2])
                        work_type = WorkType.objects.filter(code=work_type_str).first()

                        avg_work_day_str = int(long_term_hire_str[26:]) / 10
                        long_term_hire = LongTermHire.objects.create(
                            survey=self.survey,
                            work_type=work_type,
                            avg_work_day=avg_work_day_str,
                        )

                        months_str = long_term_hire_str[14:26]
                        for j in range(0, 12):
                            if months_str[j] == "1":
                                long_term_hire.months.add(
                                    Month.objects.get(value=j + 1)
                                )

                        age_str = long_term_hire_str[5:14]

                        for j in range(0, len(age_str), 3):
                            num = j / 3 + 1
                            age_scope = AgeScope.objects.get(id=num)
                            count = int(age_str[j : j + 3])

                            if count > 0:
                                NumberWorkers.objects.create(
                                    content_type=ContentType.objects.get(
                                        app_label="surveys18", model="longtermhire"
                                    ),
                                    object_id=long_term_hire.id,
                                    age_scope=age_scope,
                                    count=count,
                                )
                        self.long_term_hire.append(long_term_hire)

                except ValueError as e:
                    raise CreateModelError(target="LongTermHire", msg=e)

    def build_short_term_hire(self):
        if self.more_page is False:
            string = self.string[6]
            if len(string) % 32 != 0:
                raise StringLengthError(target="ShortTermHire")
            else:
                try:
                    self.short_term_hire = []
                    for i in range(0, len(string), 32):
                        short_term_hire_str = string[i : i + 32]
                        month_str = int(short_term_hire_str[0:2])

                        month = Month.objects.filter(value=month_str).first()
                        avg_work_day = int(short_term_hire_str[28:]) / 10

                        if month:
                            short_term_hire = ShortTermHire.objects.create(
                                survey=self.survey,
                                month=month,
                                avg_work_day=avg_work_day,
                            )

                            work_types_str = short_term_hire_str[14:28]
                            for j in range(0, len(work_types_str), 2):
                                code = int(work_types_str[j : j + 2])
                                work_type = WorkType.objects.filter(code=code).first()
                                if work_type:
                                    short_term_hire.work_types.add(work_type)

                            number_workers_str = short_term_hire_str[5:14]
                            for j in range(0, len(number_workers_str), 3):
                                num = j / 3 + 1
                                age_scope = AgeScope.objects.get(id=num)
                                count = int(number_workers_str[j : j + 3])

                                if count > 0:
                                    NumberWorkers.objects.create(
                                        content_type=ContentType.objects.get(
                                            app_label="surveys18", model="shorttermhire"
                                        ),
                                        object_id=short_term_hire.id,
                                        age_scope=age_scope,
                                        count=count,
                                    )
                            self.short_term_hire.append(short_term_hire)

                except ValueError as e:
                    raise CreateModelError(target="ShortTermHire", msg=e)

    def build_no_salary_hire(self):
        if self.more_page is False:
            string = self.string[7]

            if (len(string) - 4) % 5 != 0:
                raise StringLengthError(target="NoSalaryHire")
            else:
                try:
                    self.no_salary_hire = []
                    for i in range(0, (len(string) - 4), 5):
                        no_salary_str = string[i : i + 5]
                        month_str = no_salary_str[0:2]
                        month = Month.objects.filter(value=month_str).first()
                        count = int(no_salary_str[2:])
                        if month:
                            no_salary_hire = NoSalaryHire.objects.create(
                                survey=self.survey, month=month, count=count
                            )
                            self.no_salary_hire.append(no_salary_hire)

                except ValueError as e:
                    raise CreateModelError(target="NoSalaryHire", msg=e)

    def build_lack(self):
        if self.more_page is False:
            string = self.string[7][-4:]
            try:
                lack_str = string
                for i in range(0, len(string)):
                    if lack_str[i] == "1":
                        lack = Lack.objects.filter(id=i + 1).first()
                        if lack:
                            self.survey.lacks.add(lack)

            except ValueError as e:
                raise CreateModelError(target="Lack", msg=e)

    def build_long_term_lack(self):
        string = self.string[8]
        if len(string) % 17 != 0:
            raise StringLengthError("LongTermLack")
        else:
            if len(string) > 0:
                try:
                    self.long_term_lack = []
                    for i in range(0, len(string), 17):
                        long_term_lack_str = string[i : i + 17]
                        work_type_str = long_term_lack_str[0:2]
                        work_type = WorkType.objects.filter(code=work_type_str).first()
                        count = int(long_term_lack_str[2:5])
                        long_term_lack = LongTermLack.objects.create(
                            survey=self.survey, work_type=work_type, count=count
                        )
                        months_str = long_term_lack_str[5:]
                        for j in range(0, 12):
                            if months_str[j] == "1":
                                month = Month.objects.filter(value=j + 1).first()
                                if month:
                                    long_term_lack.months.add(month)
                        self.long_term_lack.append(long_term_lack)

                except ValueError as e:
                    raise CreateModelError(target="LongTermLack", msg=e)

    def build_short_term_lack(self):
        string = self.string[9]
        if len(string) % 21 != 0:
            raise StringLengthError("ShortTermLack")
        else:
            if len(string) > 0:
                try:
                    self.short_term_lack = []
                    for i in range(0, len(string), 21):
                        short_term_lack_str = string[i : i + 21]
                        print(short_term_lack_str)
                        product_str = short_term_lack_str[0:4]
                        product = Product.objects.filter(code=product_str).first()
                        work_type_str = short_term_lack_str[4:6]
                        work_type = WorkType.objects.filter(code=work_type_str).first()

                        count = int(short_term_lack_str[6:9])
                        short_term_lack = ShortTermLack.objects.create(
                            survey=self.survey,
                            product=product,
                            work_type=work_type,
                            count=count,
                        )
                        print(product, work_type, count)

                        months_str = short_term_lack_str[9:]
                        for j in range(0, 12):
                            if months_str[j] == "1":
                                month = Month.objects.filter(value=j + 1).first()
                                if month:
                                    short_term_lack.months.add(month)

                        self.short_term_lack.append(short_term_lack)

                except ValueError as e:
                    raise CreateModelError(target="ShortTermLack", msg=e)

    def build_subsidy(self):
        if self.more_page is False:
            string = self.string[10].split("#")

            if len(string) != 2:
                raise StringLengthError(target="Subsidy")
            else:
                try:
                    for i in range(0, 13):
                        string_1 = string[0]
                        has_subsidy_str = string_1[0:1]
                        if has_subsidy_str == "1":
                            has_subsidy = True
                        else:
                            has_subsidy = False

                        count = int(string_1[1:4])
                        month_delta = int(string_1[4:6])
                        day_delta = int(string_1[6:8])
                        hour_delta = int(string_1[8:10])

                        none_subsidy_str = string_1[10:11]
                        if none_subsidy_str == "1":
                            none_subsidy = True
                        else:
                            none_subsidy = False

                    subsidy = Subsidy.objects.create(
                        survey=self.survey,
                        has_subsidy=has_subsidy,
                        count=count,
                        month_delta=month_delta,
                        day_delta=day_delta,
                        hour_delta=hour_delta,
                        none_subsidy=none_subsidy,
                    )
                    self.subsidy = subsidy

                    self.refuse = []
                    reason_str = string[0][11:12]
                    if reason_str == "1":

                        reason = RefuseReason.objects.filter(id=1).first()
                        if reason:
                            refuse = Refuse.objects.create(
                                subsidy=self.subsidy, reason=reason
                            )

                        self.refuse.append(refuse)

                    reason_str = string[0][12:]
                    if len(reason_str) == 0:
                        raise StringLengthError(target="Subsidy")
                    elif len(reason_str) == 1:
                        if reason_str[0] == "1":
                            reason = RefuseReason.objects.filter(id=2).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy, reason=reason
                                )

                            self.refuse.append(refuse)
                    else:
                        if reason_str[0] == "1":
                            reason = RefuseReason.objects.filter(id=2).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy,
                                    reason=reason,
                                    extra=reason_str[1:],
                                )
                            self.refuse.append(refuse)

                    reason_str = string[1]
                    if len(reason_str) == 0:
                        raise StringLengthError(target="Subsidy")
                    elif len(reason_str) == 1:
                        if str.isdigit(reason_str[0]) is False:
                            raise StringLengthError(target="Subsidy")

                        if reason_str[0] == "1":
                            reason = RefuseReason.objects.filter(id=3).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy, reason=reason
                                )

                            self.refuse.append(refuse)
                    else:
                        if str.isdigit(reason_str[0]) is False:
                            raise StringLengthError(target="Subsidy")
                        if reason_str[0] == "1":
                            reason = RefuseReason.objects.filter(id=3).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy,
                                    reason=reason,
                                    extra=reason_str[1:],
                                )
                            self.refuse.append(refuse)

                except ValueError as e:
                    raise CreateModelError(target="Subsidy", msg=e)
