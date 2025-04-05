from .exceptions import (
    SignError,
    StringLengthError,
    CreateModelError,
    SurveyAlreadyExists,
)
from django.contrib.contenttypes.models import ContentType

from apps.surveys25.models import (
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
    LandArea,
    LandType,
    LandStatus,
    Loss,
    Unit,
    Product,
    Contract,
    CropMarketing,
    CityTownCode,
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
    Apply,
    ApplyResult,
    ApplyMethod,
    HireChannel,
    HireChannelItem,
    LackResponse,
    LackResponseItem,
    MaxHourlyPay,
    MaxHourlyPayItem,
)


class Builder(object):
    def __init__(self, string):
        token_size, self.is_first_page = self.check_string(string)
        delimiter_plus = "+"
        delimiter_pound = "#+"
        cut_token = []

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
        self.apply = []
        self.refuse = []
        self.hire_channel = []
        self.lack_response = []
        self.max_hourly_pay = []

        if self.is_first_page:
            for t in string.split(delimiter_plus):
                cut_token.append(t)
        else:
            tokens = string.split(delimiter_pound)
            for token in tokens:
                for t in token.split(delimiter_plus):
                    cut_token.append(t)

        self.string = cut_token

    def build(self, readonly=True, delete_exist=False):
        self.build_survey(readonly=readonly, delete_exist=delete_exist)
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
            self.build_farm_outsource()
            self.build_lack()
            self.build_subsidy()
            self.build_hire_channel()
            self.build_lack_responses()
            self.build_max_hourly_pays()
        except Exception:
            Survey.objects.filter(
                farmer_id=self.survey.farmer_id,
                page=self.survey.page,
                readonly=self.survey.readonly,
            ).delete()
            raise

    @staticmethod
    def check_string(string):
        delimiter_plus = "+"
        slices_cnt = string.count(delimiter_plus)
        if slices_cnt != 12:
            if slices_cnt != 12:
                raise SignError("+")

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
        for x in string:
            if (
                (ord(x) > 47 and ord(x) < 58)
                or (ord(x) > 64 and ord(x) < 91)
                or (ord(x) > 96 and ord(x) < 123)
            ):
                cnt = cnt + 1
                str_en_num += x
            else:
                str_ch += x

        return cnt, str_en_num, str_ch

    def build_survey(self, readonly=True, delete_exist=False):
        try:
            string = self.string[0]
            farmer_id = string[0:12]
            total_pages = int(string[12:14])
            page = int(string[14:16])
            if page == 1:
                self.is_first_page = False
            else:
                self.is_first_page = True

            if len(string) > 16 or string.count("/") == 2:
                self.is_first_page = False
                name = string[16:23].replace("#", "")
                interviewee_relationship_str = string.split("/")[1]
                interviewee_relationship = interviewee_relationship_str.split("#")[0]
                ori_class_str = string.split("/")[2]
                ori_class = int(ori_class_str[10:13])
                string = self.string[-1]
                note = string.split("#")[0]
                investigator = string.split("#")[1]
                reviewer = string.split("#")[2]
                period_m = int(string.split("#")[-1])
                string = self.string[3][-14:-12]
                main_income_source = string[0] == "1"
                non_main_income_source = string[1] == "1"

                string = self.string[10][0:2]
                # TODO: known_subsidy, non_known_subsidy should be removed and use virtual property to decide.
                non_known_subsidy = string[0] == "1"
                known_subsidy = string[1] == "1"

        except ValueError:
            raise StringLengthError("Survey")

        # dup
        exists = Survey.objects.filter(
            page=page,
            farmer_id=farmer_id,
            readonly=readonly,
        ).all()

        if exists:
            if delete_exist:
                exists.delete()
            else:
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
                    interviewee_relationship=interviewee_relationship,
                    origin_class=ori_class,
                    main_income_source=main_income_source,
                    non_main_income_source=non_main_income_source,
                    known_subsidy=known_subsidy,
                    non_known_subsidy=non_known_subsidy,
                    readonly=readonly,
                    note=note,
                    investigator=investigator,
                    reviewer=reviewer,
                    period=period_m,
                )
        except ValueError:
            raise CreateModelError("Survey")

        else:
            self.survey = survey

    def build_phone(self):
        if self.is_first_page is False:
            try:
                string = self.string[0]
                phones = string.split("/")[1:]
                phones[0] = phones[0][-10:].replace("#", "")
                phones[1] = phones[1][0:10].replace("#", "")
            except ValueError:
                raise StringLengthError("Phone")
            else:
                try:
                    for number in phones:
                        if len(number) > 0:
                            phone = Phone.objects.create(
                                survey=self.survey, phone=number
                            )
                            self.phones.append(phone)
                except ValueError:
                    raise CreateModelError("Phone")

    def build_address(self):
        match = False
        mismatch = False
        if self.is_first_page is False:
            try:
                string = self.string[0]
                string = string.split("/")[2]
                match_str = string[13:14]
                mismatch_str = string[14:15]
                address = string[15:].split("#")[0]
                if match_str == "1":
                    match = True
                if mismatch_str == "1":
                    mismatch = True
            except ValueError:
                raise StringLengthError("Address Match")
            else:
                try:
                    address = AddressMatch.objects.create(
                        survey=self.survey,
                        match=match,
                        mismatch=mismatch,
                        address=address,
                    )
                except ValueError:
                    raise CreateModelError("Address Match")
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
            except ValueError:
                raise StringLengthError("Farm Location")
            else:
                try:
                    farm_location = FarmLocation.objects.create(
                        survey=self.survey, city=city, town=town, code=code
                    )
                except ValueError:
                    raise CreateModelError("Farm Location")
                else:
                    self.farm_location = farm_location

    def build_land_area(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                area_str = string[0:31]
            except ValueError:
                raise StringLengthError("Land Area")
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

                except ValueError:
                    raise CreateModelError("Land Area")

    def build_business(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                business_str = string[31:].split("#")[0]

            except ValueError:
                raise StringLengthError("Business")
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

                except ValueError:
                    raise CreateModelError("Business")

    def build_management(self):
        if self.is_first_page is False:
            try:
                string = self.string[1]
                management_str = string[26:].split("#")[1]
                if len(management_str) != 14:
                    raise StringLengthError("management")
            except ValueError:
                raise StringLengthError("management")
            else:
                try:
                    for i in range(0, 14):
                        if management_str[i] == "1":
                            num = i + 1
                            management_type = ManagementType.objects.get(id=num)
                            self.survey.management_types.add(management_type)
                except ValueError:
                    raise CreateModelError("management")

    def build_crop_marketing(self):
        string = self.string[2]
        cnt, str_en_num, str_ch = self.counter_en_num(string)
        if cnt % 25 != 0:
            raise StringLengthError("CropMarketing")
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
                        elif has_facility_str == 0:
                            has_facility = 0
                        else:
                            has_facility = None
                        loss_str = int(crop_marketing[24:25])
                        loss = Loss.objects.filter(code=loss_str, type=1).first()
                        # print(product, name, land_number, land_area, plant_times, year_sales, has_facility, loss)

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
                except ValueError:
                    raise CreateModelError("CropMarketing")

    def build_livestock_marketing(self):
        string = self.string[3]
        if self.is_first_page is False:
            livestock_str = string[:-24]
        else:
            livestock_str = string

        cnt, str_en_num, str_ch = self.counter_en_num(livestock_str)
        if cnt % 24 != 0:
            raise StringLengthError("LivestockMarketing")
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
                except ValueError:
                    raise CreateModelError("LivestockMarketing")

    def build_annual_income(self):
        if self.is_first_page is False:
            string = self.string[3]
            annual_income_str = string[-24:]
            if len(annual_income_str) != 24:
                raise StringLengthError("AnnualIncome")
            else:
                try:
                    for i in range(0, 10, 2):
                        value = int(annual_income_str[i : i + 2])
                        if value > 0:
                            num = i / 2 + 1
                            market_type = MarketType.objects.get(id=num)
                            income_range = IncomeRange.objects.filter(id=value).first()
                            annual_income = AnnualIncome.objects.create(
                                survey=self.survey,
                                market_type=market_type,
                                income_range=income_range,
                            )
                            self.annual_income.append(annual_income)

                except ValueError:
                    raise CreateModelError("AnnualIncome")

    def build_population_age(self):
        if self.is_first_page is False:
            string = self.string[3]
            population_age_str = string[-12:]
            if len(population_age_str) != 12:
                raise StringLengthError("PopulationAge")
            else:
                try:
                    for j in range(0, len(population_age_str), 6):
                        for i in range(0, 6, 2):
                            value = int(population_age_str[i + j : i + j + 2])
                            age_scope = AgeScope.objects.get(id=int(j / 4 + 4))
                            if i / 2 == 1 and value > 0:
                                population_age = PopulationAge.objects.create(
                                    survey=self.survey,
                                    gender=Gender.objects.get(id=1),
                                    age_scope=age_scope,
                                    count=value,
                                )
                                self.population_age.append(population_age)
                            elif i / 2 == 2 and value > 0:
                                population_age = PopulationAge.objects.create(
                                    survey=self.survey,
                                    gender=Gender.objects.get(id=2),
                                    age_scope=age_scope,
                                    count=value,
                                )
                                self.population_age.append(population_age)

                except ValueError:
                    raise CreateModelError("PopulationAge")

    def build_population(self):
        string = self.string[4]
        if self.is_first_page is False:
            string = string[:-2]

        if (len(string)) % 24 != 0:
            raise StringLengthError("Population")
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

                        if life_style_cnt != 1:
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

                except ValueError:
                    raise CreateModelError("Population")

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

            except ValueError:
                raise CreateModelError("hire")

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
                        for j, value in enumerate(months_str):
                            if value == "1":
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
                                        app_label="surveys25", model="longtermhire"
                                    ),
                                    object_id=long_term_hire.id,
                                    age_scope=age_scope,
                                    count=count,
                                )
                        self.long_term_hire.append(long_term_hire)

                except ValueError:
                    raise CreateModelError("LongTermHire")

    def build_short_term_hire(self):
        if self.is_first_page is False:
            string = self.string[6]
            if len(string) % 32 != 0:
                raise StringLengthError("ShortTermHire")
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
                                age_scope = AgeScope.objects.get(id=j / 3 + 1)
                                count = int(number_workers_str[j : j + 3])

                                if count > 0:
                                    NumberWorkers.objects.create(
                                        content_type=ContentType.objects.get(
                                            app_label="surveys25", model="shorttermhire"
                                        ),
                                        object_id=short_term_hire.id,
                                        age_scope=age_scope,
                                        count=count,
                                    )
                            self.short_term_hire.append(short_term_hire)

                except ValueError:
                    raise CreateModelError("ShortTermHire")

    def build_no_salary_hire(self):
        if self.is_first_page is False:
            string = self.string[7]

            if (len(string) - 6) % 9 != 0:
                raise StringLengthError("NoSalaryHire")
            else:
                try:
                    for i in range(0, (len(string) - 6), 9):
                        no_salary_str = string[i : i + 9]
                        month_str = no_salary_str[0:2]
                        month = Month.objects.filter(value=month_str).first()
                        count = int(no_salary_str[2:5])
                        avg_work_day = int(no_salary_str[5:]) / 10
                        if month:
                            no_salary_hire = NoSalaryHire.objects.create(
                                survey=self.survey,
                                month=month,
                                count=count,
                                avg_work_day=avg_work_day,
                            )
                            self.no_salary_hire.append(no_salary_hire)

                except ValueError:
                    raise CreateModelError("NoSalaryHire")

    def build_farm_outsource(self):
        if self.is_first_page is False:
            string = self.string[7][-6:-4]
            try:
                has_farm_outsource = string[0] == "1"
                non_has_farm_outsource = string[1] == "1"

                self.survey.has_farm_outsource = has_farm_outsource
                self.survey.non_has_farm_outsource = non_has_farm_outsource
                self.survey.save()

            except ValueError:
                raise CreateModelError("Farm outsource")

    def build_lack(self):
        if self.is_first_page is False:
            string = self.string[7][-4:]
            try:
                lack_str = string
                for i in range(0, len(string)):
                    if lack_str[i] == "1":
                        lack = Lack.objects.get(id=i + 1)
                        if lack:
                            self.survey.lacks.add(lack)

            except ValueError:
                raise CreateModelError("Lack")

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
                        for j, value in enumerate(months_str):
                            if value == "1":
                                long_term_lack.months.add(
                                    Month.objects.get(value=j + 1)
                                )

                        self.long_term_lack.append(long_term_lack)

                except ValueError:
                    raise CreateModelError("LongTermLack")

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
                        for j, value in enumerate(months_str):
                            if value != "1":
                                continue
                            short_term_lack.months.add(Month.objects.get(value=j + 1))

                        self.short_term_lack.append(short_term_lack)

                except ValueError:
                    raise CreateModelError("ShortTermLack")

    def build_subsidy(self):
        if self.is_first_page is False:
            string = self.string[10].split("#")[0]
            cnt, str_en_num, str_ch = self.counter_en_num(string)
            if cnt != 26:
                raise StringLengthError("Subsidy")

            else:
                try:

                    subsidy = Subsidy.objects.create(
                        survey=self.survey,
                    )
                    self.subsidy = subsidy

                    # Build Apply objects.
                    apply_str = string[2:6]
                    for i, value in enumerate(apply_str):
                        if value != "1":
                            continue
                        if i // 2 < 1:
                           id_num = 1
                        else:
                           id_num = 3
                        apply = Apply.objects.create(
                           subsidy=self.subsidy,
                           result=ApplyResult.objects.get(id=id_num),
                           method=ApplyMethod.objects.get(id=i % 2 + 1),
                        )
                        self.apply.append(apply)

                    # Build Refuse objects.

                    def build_refuse(reason_id, method_id, extra=None):
                        """Helper function to abstract object creation."""
                        refuse = Refuse.objects.create(
                            subsidy=self.subsidy,
                            reason=RefuseReason.objects.get(id=reason_id),
                            method=ApplyMethod.objects.get(id=method_id),
                            extra=extra,
                        )
                        self.refuse.append(refuse)

                    # First row use RefuseReason constant, RefuseReason.pk=0
                    reason_str = string[0:2]
                    for i, value in enumerate(reason_str):
                        if value != "1":
                            continue
                        build_refuse(0, i % 2 + 1)

                    # RefuseReason constant, RefuseReason.pk=1-6
                    reason_str = string[6:18]
                    for i, value in enumerate(reason_str):
                        if value != "1":
                            continue
                        build_refuse(i // 2 + 1, i % 2 + 1)

                    # RefuseReason constant, RefuseReason.pk=7-10
                    reason_str = string[18]
                    if reason_str == "1":
                        build_refuse(7, 1)

                    reason_str = string[19]
                    if reason_str == "1":
                        build_refuse(8, 2)

                    reason_str = string[20]
                    if reason_str == "1":
                        build_refuse(9, 2)

                    reason_str = string[21]
                    if reason_str == "1":
                        build_refuse(10, 2)

                    reason_str = string[22]
                    if reason_str == "1":
                        build_refuse(11, 2)

                    reason_str = string[23]
                    if reason_str == "1":
                        build_refuse(12, 1)

                    reason_str = string[24]
                    if reason_str == "1":
                        build_refuse(12, 2)

                    reason_str = string[24:].split("#")[0]
                    cnt, str_en_num, str_ch = self.counter_en_num(reason_str[1:])
                    if reason_str[-1] == "1" or len(str_ch) > 0:
                        build_refuse(13, 1, str_ch if str_ch else None)

                    reason_str = self.string[10].split("#")[1]
                    cnt, str_en_num, str_ch = self.counter_en_num(reason_str[1:])
                    str_ch = str_ch.strip()
                    if reason_str[-1] == "1" or len(str_ch) > 0:
                        build_refuse(13, 2, str_ch if str_ch else None)

                except ValueError:
                    raise CreateModelError("Subsidy")

    def build_hire_channel(self):
        if self.is_first_page is False:
            try:
                string = self.string[11].split("#")[0]

            except ValueError:
                raise StringLengthError("HireChannel")
            else:
                try:
                    for i in range(0, 6):
                        if string[i] == "1":
                            num = i + 1
                            hire_channel = HireChannel.objects.create(
                                survey=self.survey,
                                item=HireChannelItem.objects.get(
                                    code=num
                                ),
                            )
                            self.hire_channel.append(hire_channel)
                    if string[6] == "1":
                        hire_channel = HireChannel.objects.create(
                            survey=self.survey,
                            item=HireChannelItem.objects.get(
                                code=7
                            ),
                            extra=string[7:],
                        )
                        self.hire_channel.append(hire_channel)
                    elif len(string[6:]) > 2:
                        hire_channel = HireChannel.objects.create(
                            survey=self.survey, extra=string[7:]
                        )
                        self.hire_channel.append(hire_channel)

                except ValueError:
                    raise CreateModelError("HireChannel")

    def build_lack_responses(self):
        if self.is_first_page is False:
            try:
                string = self.string[11].split("#")[1]

            except ValueError:
                raise StringLengthError("LackResponses")
            else:
                try:
                    for i in range(0, 8):
                        if string[i] == "1":
                            num = i + 1
                            lack_response = LackResponse.objects.create(
                                survey=self.survey,
                                item=LackResponseItem.objects.get(
                                    code=num
                                ),
                            )
                            self.lack_response.append(lack_response)
                    if string[8] == "1":
                        lack_response = LackResponse.objects.create(
                            survey=self.survey,
                            item=LackResponseItem.objects.get(
                                code=9
                            ),
                            extra=string[9:],
                        )
                        self.lack_response.append(lack_response)
                    elif len(string[8:]) > 2:
                        lack_response = LackResponse.objects.create(
                            survey=self.survey, extra=string[9:]
                        )
                        self.lack_responses.append(lack_response)

                except ValueError:
                    raise CreateModelError("LackResponses")

    def build_max_hourly_pays(self):
        if self.is_first_page is False:
            try:
                string = self.string[11].split("#")[2]

            except ValueError:
                raise StringLengthError("MaxHourlyPayItem")
            else:
                try:
                    for i in range(0, 7):
                        if string[i] == "1":
                            num = i + 1
                            max_hourly_pay = MaxHourlyPay.objects.create(
                                survey=self.survey,
                                item=MaxHourlyPayItem.objects.get(
                                    code=num
                                ),
                            )
                            self.max_hourly_pay.append(max_hourly_pay)
                    if string[7] == "1":
                        max_hourly_pay = MaxHourlyPay.objects.create(
                            survey=self.survey,
                            item=MaxHourlyPayItem.objects.get(
                                code=8
                            ),
                            extra=string[8:],
                        )
                        self.max_hourly_pay.append(max_hourly_pay)
                    elif len(string[7:]) > 2:
                        max_hourly_pay = MaxHourlyPay.objects.create(
                            survey=self.survey, extra=string[8:]
                        )
                        self.max_hourly_pay.append(max_hourly_pay)

                except ValueError:
                    raise CreateModelError("MaxHourlyPayItem")
