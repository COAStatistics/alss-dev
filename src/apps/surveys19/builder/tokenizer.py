from .exceptions import SignError, StringLengthError, CreateModelError, SurveyAlreadyExists
from django.contrib.contenttypes.models import ContentType

from apps.surveys19.models import (
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
    FarmLocation,
    CityTownCode,
    LandArea,
    LandType,
    LandStatus,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    LivestockMarketing,
    PopulationAge,
    Population,
    EducationLevel,
    FarmerWorkDay,
    LifeStyle,
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
    Relationship,
    Month,
    Refuse,
)


class Builder(object):
    def __init__(self, string, delete_exist=False):
        token_size, self.is_first_page = self.check_string(string)
        delimiter_plus = "+"
        delimiter_pound = "#+"
        cut_token = []

        self.delete_exist = delete_exist
        self.survey = None
        self.phones = []
        self.address = None
        self.farm_location = None
        self.land_area = []
        self.business = []
        self.crop_marketing = []
        self.livestock_marketing = []
        self.annual_income = []
        self.population_age = []
        self.population = []
        self.long_term_hire = []
        self.short_term_hire = []
        self.no_salary_hire = []
        self.long_term_lack = []
        self.short_term_lack = []
        self.subsidy = None
        self.refuse = []

        if self.is_first_page:
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
            self.build_farm_location()
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
                if slices_pound_cnt != 1:
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
        index = 0
        for i in range(0, len(string)):
            if string[i] == "1":
                index = i + 1
                cnt = cnt + 1
        return cnt, index

    @staticmethod
    def counter_en_num(string):
        cnt = 0
        str_en_num = ""
        str_ch = ""
        for i in range(0, len(string)):
            if (
                string[i].isdigit()
                or ord(string[i]) > 64
                and ord(string[i]) < 91
                or (ord(string[i]) > 96 and ord(string[i]) < 123)
            ):
                cnt = cnt + 1
                str_en_num += string[i]
            else:
                str_ch += string[i]
        return cnt, str_en_num, str_ch

    def build_survey(self, readonly=True):
        try:
            string = self.string[0]
            farmer_id = string[0:12]
            total_pages = int(string[12:14])
            page = int(string[14:16])
            if len(self.string[0]) > 16:
                self.is_first_page = False
                name = string[16:23].replace("#", "")
                ori_class = int(string[44:46])
                string = self.string[-1]
                note = string.split("#")[0]
                investigator = string.split("#")[1]
                reviewer = string.split("#")[2]
                period_m = int(string.split("#")[-1])
                second_str = self.string[1][-2]
                non_second_str = self.string[1][-1]
                second = second_str == "1"
                non_second = non_second_str == "1"

        except ValueError as e:
            raise StringLengthError(model_name="Survey", msg=e)

        # dup
        exists = Survey.objects.filter(
            page=page, farmer_id=farmer_id
        ).all()

        if exists:
            if self.delete_exist:
                exists.delete()
            raise SurveyAlreadyExists()

        try:
            if self.is_first_page:
                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    page=page,
                    total_pages=total_pages,
                    readonly=readonly,
                )
            else:
                survey = Survey.objects.create(
                    farmer_id=farmer_id,
                    page=page,
                    total_pages=total_pages,
                    farmer_name=name,
                    origin_class=ori_class,
                    second=second,
                    non_second=non_second,
                    readonly=readonly,
                    note=note,
                    investigator=investigator,
                    reviewer=reviewer,
                    period=period_m,
                )
        except ValueError as e:
            raise CreateModelError(model_name="Survey", msg=e)

        else:
            self.survey = survey

    def build_phone(self):
        if self.is_first_page is False:
            try:
                string = self.string[0]
                phones = string[23:44].replace("#", "").split("/")
            except ValueError as e:
                raise StringLengthError(model_name="Phone", msg=e)
            else:
                try:
                    for number in phones:
                        if len(number) > 0:
                            phone = Phone.objects.create(
                                survey=self.survey, phone=number
                            )
                            self.phones.append(phone)
                except ValueError as e:
                    raise CreateModelError(model_name="Phone", msg=e)

    def build_address(self):
        match = False
        mismatch = False
        if self.is_first_page is False:
            try:
                string = self.string[0]
                match_str = string[46:47]
                mismatch_str = string[47:48]
                address = string[48:].split("#")[0]
                if match_str == "1":
                    match = True
                if mismatch_str == "1":
                    mismatch = True
            except ValueError as e:
                raise StringLengthError(model_name="Address Match", msg=e)
            else:
                try:
                    address = AddressMatch.objects.create(
                        survey=self.survey,
                        match=match,
                        mismatch=mismatch,
                        address=address,
                    )
                except ValueError as e:
                    raise CreateModelError(model_name="Address Match", msg=e)
                else:
                    self.address = address

    def build_farm_location(self):
        if self.is_first_page is False:
            try:
                string = self.string[0]
                token = string.split("#")
                city = token[-3]
                town = token[-2]
                code_str = int(token[-1])
                code = CityTownCode.objects.filter(code=code_str).first()
            except ValueError as e:
                raise StringLengthError(model_name="Farm Location", msg=e)
            else:
                try:
                    farm_location = FarmLocation.objects.create(
                        survey=self.survey, city=city, town=town, code=code
                    )
                except ValueError as e:
                    raise CreateModelError(model_name="Farm Location", msg=e)
                else:
                    self.farm_location = farm_location

    def build_land_area(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                area_str = string[0:26]
            except ValueError as e:
                raise StringLengthError(model_name="Land Area", msg=e)
            else:
                try:
                    cnt = 0
                    for i in range(5, len(area_str), 5):
                        if int(area_str[cnt * 5 : i]) > 0:
                            land_type = 1 if cnt < 3 else 2
                            status = int(i / 5) - 3 if i / 5 > 3 else int(i / 5)

                            land_type = LandType.objects.get(id=land_type)
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
                    raise CreateModelError(model_name="Land Area", msg=e)

    def build_business(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                business_str = string[26:].split("#")[0]

            except ValueError as e:
                raise StringLengthError(model_name="Business", msg=e)
            else:
                try:
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
                    raise CreateModelError(model_name="Business", msg=e)

    def build_management(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                management_str = string[26:].split("#")[1]
                if len(management_str) != 16:
                    raise StringLengthError(model_name="management")
            except ValueError as e:
                raise StringLengthError(model_name="management", msg=e)
            else:
                try:
                    for i in range(0, 14):
                        if management_str[i] == "1":
                            num = i + 1
                            management_type = ManagementType.objects.get(id=num)
                            self.survey.management_types.add(management_type)
                except ValueError as e:
                    raise CreateModelError(model_name="management", msg=e)

    def build_crop_marketing(self):
        string = self.string[2]
        cnt, str_en_num, str_ch = self.counter_en_num(string)
        if cnt % 25 != 0:
            raise StringLengthError(model_name="CropMarketing")
        else:
            if len(string) > 0:
                try:
                    num = int(len(str_en_num) / 25)
                    for i in range(0, num):
                        crop_marketing = str_en_num[i * 25 : i * 25 + 25]
                        product_str = crop_marketing[0:3]
                        name = str_ch.split("#")[i]
                        product = Product.objects.filter(code=product_str).first()
                        land_number = int(crop_marketing[3:4])
                        land_area = int(crop_marketing[4:9])
                        plant_times = int(crop_marketing[9:10])
                        if crop_marketing[10:11].isdigit():
                            unit_str = int(crop_marketing[10:11])
                            unit = Unit.objects.filter(code=unit_str, type=1).first()
                        else:
                            unit = None

                        year_sales = int(crop_marketing[11:23])
                        has_facility_str = int(crop_marketing[23:24])

                        if has_facility_str == 1:
                            has_facility = 1
                        elif has_facility_str == 2:
                            has_facility = 0
                        else:
                            has_facility = None
                        loss_str = int(crop_marketing[24:25])
                        loss = Loss.objects.filter(code=loss_str, type=1).first()
                        print(product, name, land_number, land_area, plant_times, unit, year_sales, has_facility, loss)

                        crop_marketing = CropMarketing.objects.create(
                            survey=self.survey,
                            product=product,
                            name=name,
                            land_number=land_number,
                            land_area=land_area,
                            plant_times=plant_times,
                            unit=unit,
                            year_sales=year_sales,
                            has_facility=has_facility,
                            loss=loss,
                        )
                        self.crop_marketing.append(crop_marketing)
                except ValueError as e:
                    raise CreateModelError(model_name="CropMarketing", msg=e)

    def build_livestock_marketing(self):
        string = self.string[3]
        if self.is_first_page is False:
            livestock_str = string[:-22]
        else:
            livestock_str = string

        cnt, str_en_num, str_ch = self.counter_en_num(livestock_str)
        if cnt % 24 != 0:
            raise StringLengthError(model_name="LivestockMarketing")
        else:
            if cnt > 0:
                try:
                    num = int(cnt / 24)
                    for i in range(0, num):
                        livestock = str_en_num[i * 24 : i * 24 + 24]
                        product_str = livestock[0:3]
                        name = str_ch.split("#")[i]
                        product = Product.objects.filter(code=product_str).first()
                        unit_str = int(livestock[3:4])
                        unit = Unit.objects.filter(code=unit_str, type=2).first()
                        raising_number = int(livestock[4:10])
                        year_sales = int(livestock[10:22])
                        contract_str = int(livestock[22:23])
                        contract = Contract.objects.filter(code=contract_str).first()
                        loss_str = int(livestock[23:24])
                        loss = Loss.objects.filter(code=loss_str, type=2).first()

                        livestock_marketing = LivestockMarketing.objects.create(
                            survey=self.survey,
                            product=product,
                            name=name,
                            unit=unit,
                            raising_number=raising_number,
                            year_sales=year_sales,
                            contract=contract,
                            loss=loss,
                        )
                        self.livestock_marketing.append(livestock_marketing)
                except ValueError as e:
                    raise CreateModelError(model_name="LivestockMarketing", msg=e)

    def build_annual_income(self):
        if self.is_first_page is False:
            string = self.string[3]
            annual_income_str = string[-22:]
            if len(annual_income_str) != 22:
                raise StringLengthError(model_name="AnnualIncome")
            else:
                try:
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
                    raise CreateModelError(model_name="AnnualIncome", msg=e)

    def build_population_age(self):
        if self.is_first_page is False:
            string = self.string[3]
            population_age_str = string[-12:]
            if len(population_age_str) != 12:
                raise StringLengthError(model_name="PopulationAge")
            else:
                try:
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
                    raise CreateModelError(model_name="PopulationAge", msg=e)

    def build_population(self):
        string = self.string[4]
        if self.is_first_page is False:
            string = string[:-2]

        if (len(string)) % 24 != 0:
            raise StringLengthError(model_name="Population")
        else:
            if len(string) > 0:
                try:
                    for i in range(0, len(string), 24):
                        population_str = string[i : i + 24]
                        relationship_str = int(population_str[2:3])

                        relationship = Relationship.objects.filter(
                            code=relationship_str
                        ).first()
                        gender_str = int(population_str[3:4])
                        gender = Gender.objects.filter(code=gender_str).first()

                        birth_year = int(population_str[4:7])
                        education_level_str = int(population_str[7:8])
                        education_level = EducationLevel.objects.filter(
                            code=education_level_str
                        ).first()
                        farmer_work_day_str = population_str[8:16]
                        farmer_work_day_cnt, farmer_work_day_id = self.id_and_value(
                            farmer_work_day_str
                        )
                        if farmer_work_day_cnt != 1:
                            farmer_work_day = None
                        else:
                            farmer_work_day = FarmerWorkDay.objects.filter(
                                code=farmer_work_day_id
                            ).first()

                        life_style_str = population_str[16:]
                        life_style_cnt, life_style_id = self.id_and_value(
                            life_style_str
                        )

                        if farmer_work_day_cnt != 1:
                            life_style = None
                        else:
                            life_style = LifeStyle.objects.filter(
                                code=life_style_id
                            ).first()
                        population = Population.objects.create(
                            survey=self.survey,
                            relationship=relationship,
                            gender=gender,
                            birth_year=birth_year,
                            education_level=education_level,
                            farmer_work_day=farmer_work_day,
                            life_style=life_style,
                        )
                        self.population.append(population)

                except ValueError as e:
                    raise CreateModelError(model_name="Population", msg=e)

    def build_hire(self):
        if self.is_first_page is False:
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

            except ValueError as e:
                raise CreateModelError(model_name="hire", msg=e)

    def build_long_term_hire(self):
        string = self.string[5]
        if len(string) % 30 != 0:
            raise StringLengthError("LongTermHire")
        else:
            if len(string) > 0:
                try:
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
                                        app_label="surveys19", model="longtermhire"
                                    ),
                                    object_id=long_term_hire.id,
                                    age_scope=age_scope,
                                    count=count,
                                )
                        self.long_term_hire.append(long_term_hire)

                except ValueError as e:
                    raise CreateModelError(model_name="LongTermHire", msg=e)

    def build_short_term_hire(self):
        if self.is_first_page is False:
            string = self.string[6]
            if len(string) % 32 != 0:
                raise StringLengthError(model_name="ShortTermHire")
            else:
                try:
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
                                            app_label="surveys19", model="shorttermhire"
                                        ),
                                        object_id=short_term_hire.id,
                                        age_scope=age_scope,
                                        count=count,
                                    )
                            self.short_term_hire.append(short_term_hire)

                except ValueError as e:
                    raise CreateModelError(model_name="ShortTermHire", msg=e)

    def build_no_salary_hire(self):
        if self.is_first_page is False:
            string = self.string[7]

            if (len(string) - 4) % 5 != 0:
                raise StringLengthError(model_name="NoSalaryHire")
            else:
                try:
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
                    raise CreateModelError(model_name="NoSalaryHire", msg=e)

    def build_lack(self):
        if self.is_first_page is False:
            string = self.string[7][-4:]
            try:
                lack_str = string
                for i in range(0, len(string)):
                    if lack_str[i] == "1":
                        lack = Lack.objects.filter(id=i + 1).first()
                        if lack:
                            self.survey.lacks.add(lack)

            except ValueError as e:
                raise CreateModelError(model_name="Lack", msg=e)

    def build_long_term_lack(self):
        string = self.string[8]
        if len(string) % 21 != 0:
            raise StringLengthError("LongTermLack")
        else:
            if len(string) > 0:
                try:
                    for i in range(0, len(string), 21):
                        long_term_lack_str = string[i : i + 21]
                        work_type_str = long_term_lack_str[0:2]
                        work_type = WorkType.objects.filter(code=work_type_str).first()
                        count = int(long_term_lack_str[2:5])
                        avg_lack_day = int(long_term_lack_str[17:]) / 10

                        long_term_lack = LongTermLack.objects.create(
                            survey=self.survey,
                            work_type=work_type,
                            count=count,
                            avg_lack_day=avg_lack_day,
                        )
                        months_str = long_term_lack_str[5:17]
                        for j in range(0, 12):
                            if months_str[j] == "1":
                                month = Month.objects.filter(value=j + 1).first()
                                if month:
                                    long_term_lack.months.add(month)

                        self.long_term_lack.append(long_term_lack)

                except ValueError as e:
                    raise CreateModelError(model_name="LongTermLack", msg=e)

    def build_short_term_lack(self):
        string = self.string[9]
        cnt, str_en_num, str_ch = self.counter_en_num(string)

        if cnt % 24 != 0:
            raise StringLengthError("ShortTermLack")
        else:
            if len(string) > 0:
                try:
                    num = int(cnt / 24)
                    for i in range(0, num):
                        token = str_en_num[i * 24 : i * 24 + 24]
                        product_str = token[0:3]
                        name = str_ch.split("#")[i]
                        product = Product.objects.filter(code=product_str).first()
                        work_type_str = token[3:5]
                        work_type = WorkType.objects.filter(code=work_type_str).first()

                        count = int(token[5:8])
                        avg_lack_day = int(token[20:]) / 10

                        short_term_lack = ShortTermLack.objects.create(
                            survey=self.survey,
                            product=product,
                            work_type=work_type,
                            name=name,
                            avg_lack_day=avg_lack_day,
                            count=count,
                        )

                        months_str = token[8:20]
                        for j in range(0, 12):
                            if months_str[j] == "1":
                                month = Month.objects.filter(value=j + 1).first()
                                if month:
                                    short_term_lack.months.add(month)

                        self.short_term_lack.append(short_term_lack)

                except ValueError as e:
                    raise CreateModelError(model_name="ShortTermLack", msg=e)

    def build_subsidy(self):
        if self.is_first_page is False:
            string = self.string[10].split("#")
            cnt, str_en_num, str_ch = self.counter_en_num(self.string[10])

            if len(string) != 2 or cnt != 12:
                raise StringLengthError(model_name="Subsidy")
            else:
                try:
                    string_1 = string[0]
                    has_subsidy_str = string_1[0:1]
                    has_subsidy = has_subsidy_str == "1"

                    count = int(string_1[1:4])
                    month_delta = int(string_1[4:6])
                    day_delta = int(string_1[6:8])

                    none_subsidy_str = string_1[8:9]
                    none_subsidy = none_subsidy_str == "1"

                    subsidy = Subsidy.objects.create(
                        survey=self.survey,
                        has_subsidy=has_subsidy,
                        count=count,
                        month_delta=month_delta,
                        day_delta=day_delta,
                        none_subsidy=none_subsidy,
                    )
                    self.subsidy = subsidy
                    reason_str = string[0][9:10]
                    if reason_str == "1":
                        reason = RefuseReason.objects.filter(id=1).first()
                        if reason:
                            refuse = Refuse.objects.create(
                                subsidy=self.subsidy, reason=reason
                            )

                        self.refuse.append(refuse)

                    reason_str = string[0][10:]
                    if len(reason_str) == 0:
                        raise StringLengthError(model_name="Subsidy")
                    elif len(reason_str) > 0:
                        if reason_str[0:1] == "1" and len(reason_str) == 2:
                            reason = RefuseReason.objects.filter(id=2).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy, reason=reason
                                )

                            self.refuse.append(refuse)

                        elif len(reason_str) > 1:
                            if reason_str[0:1].isdigit() is False:
                                raise StringLengthError(model_name="Subsidy")
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
                        raise StringLengthError(model_name="Subsidy")
                    elif len(reason_str) > 0:

                        if reason_str[0] == "1" and len(reason_str) == 0:
                            reason = RefuseReason.objects.filter(id=3).first()
                            if reason:
                                refuse = Refuse.objects.create(
                                    subsidy=self.subsidy, reason=reason
                                )

                            self.refuse.append(refuse)
                        elif len(reason_str) > 1:
                            if reason_str[0:1].isdigit() is False:
                                raise StringLengthError(model_name="Subsidy")
                            else:
                                reason = RefuseReason.objects.filter(id=3).first()
                                if reason:
                                    refuse = Refuse.objects.create(
                                        subsidy=self.subsidy,
                                        reason=reason,
                                        extra=reason_str[1:],
                                    )
                                self.refuse.append(refuse)

                except ValueError as e:
                    raise CreateModelError(model_name="Subsidy", msg=e)
