import operator
import logging
from functools import reduce
from itertools import islice
from collections import namedtuple

from django.db.models import Count, Q

from apps.surveys20.models import (
    Survey,
    LandArea,
    Business,
    ManagementType,
    CropMarketing,
    LivestockMarketing,
    AnnualIncome,
    AgeScope,
    PopulationAge,
    Population,
    LongTermHire,
    ShortTermHire,
    NoSalaryHire,
    Lack,
    LongTermLack,
    ShortTermLack,
    Refuse,
)

logging.getLogger(__file__).setLevel(logging.INFO)


class SurveyRelationGeneratorFactory108:
    """ Generator Factory of Survey Relations. """

    ExportRelation = namedtuple("ExportRelation", ("generator", "column_count"))

    def __init__(self, readonly=False, filters={}, excludes={}):
        """ Make the necessary query, initial the relations in constrains and ordering by farmer_id """
        self.readonly = readonly
        self.filters = filters
        self.excludes = excludes

        self.surveys = (
            self.get_queryset(
                Survey.objects.prefetch_related(
                    "phones", "address_match", "farm_location"
                ),
                filter_by_farmer_ids=False,
            )
            .filter(page=1)
            .all()
        )
        self.farmer_ids = self.surveys.values_list("farmer_id", flat=True).distinct()

        self.lookup_tables = [
            "land_areas",
            "businesses",
            "management_types",
            "lacks",
            "crop_marketings",
            "livestock_marketings",
            "annual_incomes",
            "population_ages",
            "populations",
            "long_term_hires",
            "short_term_hires",
            "no_salary_hires",
            "no_salary_hires",
            "long_term_lacks",
            "short_term_lacks",
            "subsidy__refuses",
        ]
        self.relation_count_mapping = self.get_relations_count_mapping()
        self.age_scopes = AgeScope.objects.filter(group=1).order_by("id").all()

        self.land_areas = self.ExportRelation(
            self.relation_generate(
                LandArea, ["type__name", "status__name", "value"], ["type", "status"]
            ),
            3,
        )
        self.businesses = self.ExportRelation(
            self.relation_generate(
                Business,
                ["farm_related_business__name", "extra"],
                ["farm_related_business"],
            ),
            2,
        )
        self.management_types = self.ExportRelation(
            self.relation_generate(ManagementType, ["name"], many_to_many=True), 1
        )
        self.crop_marketings = self.ExportRelation(
            self.relation_generate(
                CropMarketing,
                [
                    "product__code",
                    "name",
                    "land_number",
                    "land_area",
                    "plant_times",
                    "unit__name",
                    "year_sales",
                    "has_facility",
                    "loss__name",
                ],
                [
                    "product",
                    "unit",
                    "loss",
                ],
            ),
            9,
        )
        self.livestock_marketings = self.ExportRelation(
            self.relation_generate(
                LivestockMarketing,
                [
                    "product__code",
                    "name",
                    "unit__name",
                    "raising_number",
                    "year_sales",
                    "contract__name",
                    "loss__name",
                ],
                [
                    "product",
                    "unit",
                    "contract",
                    "loss",
                ],
            ),
            7,
        )
        self.annual_incomes = self.ExportRelation(
            self.relation_generate(
                AnnualIncome,
                ["market_type__name", "income_range__name"],
                ["market_type", "income_range"],
            ),
            2,
        )
        self.population_ages = self.ExportRelation(
            self.relation_generate(
                PopulationAge,
                [
                    "age_scope__name",
                    "gender__name",
                    "count",
                ],
                [
                    "age_scope",
                    "gender",
                ],
            ),
            3,
        )
        self.populations = self.ExportRelation(
            self.relation_generate(
                Population,
                [
                    "relationship__name",
                    "gender__name",
                    "birth_year",
                    "education_level__name",
                    "farmer_work_day",
                    "life_style__name",
                ],
                ["relationship", "gender", "education_level", "life_style"],
            ),
            6,
        )
        self.no_salary_hires = self.ExportRelation(
            self.relation_generate(NoSalaryHire, ["month__value", "count"], ["month"]),
            2,
        )
        self.lacks = self.ExportRelation(
            self.relation_generate(Lack, ["name"], many_to_many=True), 1
        )
        self.long_term_hires = self.ExportRelation(
            self.long_term_hires_generate(), 4 + len(self.age_scopes)
        )
        self.short_term_hires = self.ExportRelation(
            self.short_term_hires_generate(), 4 + len(self.age_scopes)
        )
        self.long_term_lacks = self.ExportRelation(self.long_term_lacks_generate(), 4)
        self.short_term_lacks = self.ExportRelation(self.short_term_lacks_generate(), 6)
        self.subsidy__refuses = self.ExportRelation(self.refuses_generate(), 1)

    def check_exhausted(self):
        return all(
            [
                len(list(getattr(self, relation).generator)) == 0
                for relation in self.lookup_tables
            ]
        )

    def check_relation(self, relation):
        mapping_sum = sum(
            [
                self.relation_count_mapping[farmer_id][relation]
                for farmer_id in self.farmer_ids
            ]
        )
        relation_count = len(list(getattr(self, relation).generator))
        if mapping_sum != relation_count:
            print(
                f"Relation {relation} not fit: Mapping Sum={mapping_sum}; Relation Count={relation_count}"
            )
            return False
        return True

    def get_queryset(self, qs, prefix="", filter_by_farmer_ids=True):
        """ Apply common filter and ordering for relation querysets """
        _default_filters = {f"{prefix}readonly": self.readonly}
        if filter_by_farmer_ids:
            # Single survey is split into multiple Survey objects and share same farmer_id
            # The relation tables still need to filter by farmer_id
            # In case the filter/exclude below not working properly
            _default_filters[f"{prefix}farmer_id__in"] = self.farmer_ids
        _filters = {f"{prefix}{key}": value for key, value in self.filters.items()}
        _excludes = {f"{prefix}{key}": value for key, value in self.excludes.items()}
        _default_order_by = f"{prefix}farmer_id"
        return qs.filter(
            reduce(
                operator.and_, [Q(**_default_filters), Q(**_filters), ~Q(**_excludes)]
            )
        ).order_by(_default_order_by)

    def relation_generate(
        self, model, values_list, prefetch_relates=[], many_to_many=False
    ):
        """ Get the iterator of relation object values """
        prefix = "surveys__" if many_to_many else "survey__"
        qs = self.get_queryset(
            model.objects.prefetch_related(*prefetch_relates).all(), prefix=prefix
        )
        return qs.values_list(*values_list).iterator()

    def get_sliced_relation_generator(self, farmer_id, relate_name):
        """ Consume the generator on at a time, base on the relation count mapping """
        mapping_info = self.relation_count_mapping[farmer_id]
        relation_count = mapping_info[relate_name]
        max_relation_count = max(mapping_info.values())
        relation = getattr(self, relate_name)
        yield from islice(relation.generator, 0, relation_count)
        for _ in range(max_relation_count - relation_count):
            yield [""] * relation.column_count

    def long_term_hires_generate(self):
        qs = self.get_queryset(
            LongTermHire.objects.prefetch_related(
                "work_type", "months", "number_workers"
            ).all(),
            prefix="survey__",
        )
        for lth in qs.iterator():
            values = [
                lth.work_type.name,
                lth.avg_work_day,
                ",".join(map(str, lth.months.values_list("value", flat=True))),
            ]
            worker_list = list()
            for age_scope in self.age_scopes:
                search = lth.number_workers.filter(age_scope=age_scope).first()
                worker_list.append(search.count if search else 0)
            values.append(sum(worker_list))
            values += worker_list
            yield tuple(values)

    def short_term_hires_generate(self):
        qs = self.get_queryset(
            ShortTermHire.objects.prefetch_related(
                "work_types", "number_workers", "month"
            ).all(),
            prefix="survey__",
        )
        for sth in qs.iterator():
            values = [
                ",".join(map(str, sth.work_types.values_list("name", flat=True))),
                sth.avg_work_day,
                sth.month.value,
            ]
            worker_list = list()
            for age_scope in self.age_scopes:
                search = sth.number_workers.filter(age_scope=age_scope).first()
                worker_list.append(search.count if search else 0)
            values.append(sum(worker_list))
            values += worker_list
            yield tuple(values)

    def long_term_lacks_generate(self):
        qs = self.get_queryset(
            LongTermLack.objects.prefetch_related("work_type").all(), prefix="survey__"
        )
        for ltl in qs.iterator():
            yield (
                ltl.work_type.name,
                ltl.count,
                ltl.avg_lack_day,
                ",".join(map(str, ltl.months.values_list("value", flat=True))),
            )

    def short_term_lacks_generate(self):
        qs = self.get_queryset(
            ShortTermLack.objects.prefetch_related("work_type", "product").all(),
            prefix="survey__",
        )
        for obj in qs.iterator():
            yield (
                obj.work_type.name,
                obj.product.code,
                obj.name,
                obj.count,
                obj.avg_lack_day,
                ",".join(map(str, obj.months.values_list("value", flat=True))),
            )

    def refuses_generate(self):
        qs = self.get_queryset(
            Refuse.objects.prefetch_related("reason").all(), prefix="subsidy__survey__"
        )
        for obj in qs.iterator():
            yield (f"{obj.reason.name}({obj.extra})" if obj.extra else obj.reason.name,)

    def get_relations_count_mapping(self):
        """ Lazy pre-calculate relation counts for each farmer id """
        result = {}
        qs = self.get_queryset(Survey.objects.all())

        def count_relation(relate_name):
            relations_count = (
                qs.values("farmer_id")
                .annotate(count=Count(relate_name))
                .values_list("farmer_id", "count")
                .order_by("farmer_id")
                .iterator()
            )
            return relations_count

        generator_lists = [count_relation(table) for table in self.lookup_tables]

        while True:
            try:
                single_result = [next(generator) for generator in generator_lists]
                farmer_id = single_result[1][0]
                result[farmer_id] = {
                    self.lookup_tables[i]: item[1]
                    for i, item in enumerate(single_result)
                }
            except StopIteration:
                break

        return result

    def export_generator(self):
        """ Main generator for exporting """

        def output_formatter(value):
            if isinstance(value, bool):
                value = "是" if value else "否"
            if value is None:
                value = ""
            return str(value)

        errors = []
        headers = [
            "農戶編號",
            "受訪人姓名",
            "與名冊戶長關係",  # new 108
            "電話1",
            "電話2",
            "地址與名冊相不相同",
            "地址",
            "可耕地或畜牧用地所在地區",
            "可耕地或畜牧用地所在地區代號",  # new 108
            "有無二代青農",
            "耕作地類型",
            "耕作地狀態",
            "耕作地面積",
            "兼營農業相關事業",
            "其他填寫",
            "主要經營型態",
            "作物代碼",
            "作物名稱",
            "耕作地編號",
            "種植面積",
            "種植次數",
            "計量單位",
            "全年銷售額",
            "是否使用農業設施",
            "作物備註",
            "畜禽代碼",
            "畜禽名稱",
            "計量單位",
            "年底在養數量",
            "全年銷售額",
            "契約飼養",
            "畜禽備註",
            "銷售類型",
            "銷售額區間",
            "全年主要淨收入來源",  # new 108
            "年齡分類",  # new 108
            "戶內人口性別",  # new 108
            "戶內人口數",  # new 108
            "與經濟戶長關係",
            "性別",
            "出生年",
            "教育程度別",
            "自家農牧業工作日數",
            "全年主要生活型態",
            "僱工情形",  # new 108
            "常僱主要工作類型",
            "常僱平均工作日數",
            "常僱月份",
            "常僱合計",  # new 108
            "常僱(44歲以下)",
            "常僱(45-64歲)",
            "常僱(65歲以上)",
            "臨僱主要工作類型",
            "臨僱平均工作日數",
            "臨僱月份",
            "臨僱合計",  # new 108
            "臨僱(44歲以下)",
            "臨僱(45-64歲)",
            "臨僱(65歲以上)",
            "不支薪僱用月份",
            "不支薪人數",
            "短缺情形",
            "常缺工作類型",
            "常缺各月人數",
            "常缺各月平均日數",
            "常缺月份",
            "臨缺工作類型",
            "臨缺產品代碼",
            "臨缺產品名稱",
            "臨缺各月人數",
            "臨缺各月平均日數",
            "臨缺月份",
            "是否聽過人力團",  # new 108
            "是否有申請人力團",  # new 108
            "無申請人力團原因",  # new 108
            # "有無申請缺工2.0",
            # "申請人數",
            # "申請總時間(日)",
            # "無申請缺工2.0原因",
            "調查員",
            "複審員",
        ]

        yield headers

        for survey in self.surveys:
            try:
                block1 = [
                    survey.farmer_id,
                    survey.farmer_name,
                    survey.interviewee_relationship,
                    survey.phones.first().phone,
                    survey.phones.last().phone,
                    survey.address_match.match,
                    survey.address_match.address,
                    survey.farm_location.city + survey.farm_location.town,
                    survey.farm_location.code,
                    survey.second,
                ]
                block2 = [
                    "以自家農牧業淨收入為主" if survey.main_income_source else "以自家農牧業外淨收入為主",
                ]
                block3 = [
                    "2" if survey.hire else "1",
                ]
                block4 = [
                    "1" if survey.known_subsidy else "0",
                    "1" if survey.subsidy.has_subsidy else "0",
                ]
                block5 = [
                    survey.investigator,
                    survey.reviewer,
                ]
                land_areas = self.get_sliced_relation_generator(
                    survey.farmer_id, "land_areas"
                )
                businesses = self.get_sliced_relation_generator(
                    survey.farmer_id, "businesses"
                )
                management_types = self.get_sliced_relation_generator(
                    survey.farmer_id, "management_types"
                )
                crop_marketings = self.get_sliced_relation_generator(
                    survey.farmer_id, "crop_marketings"
                )
                livestock_marketings = self.get_sliced_relation_generator(
                    survey.farmer_id, "livestock_marketings"
                )
                annual_incomes = self.get_sliced_relation_generator(
                    survey.farmer_id, "annual_incomes"
                )
                population_ages = self.get_sliced_relation_generator(
                    survey.farmer_id, "population_ages"
                )
                populations = self.get_sliced_relation_generator(
                    survey.farmer_id, "populations"
                )
                long_term_hires = self.get_sliced_relation_generator(
                    survey.farmer_id, "long_term_hires"
                )
                short_term_hires = self.get_sliced_relation_generator(
                    survey.farmer_id, "short_term_hires"
                )
                no_salary_hires = self.get_sliced_relation_generator(
                    survey.farmer_id, "no_salary_hires"
                )
                long_term_lacks = self.get_sliced_relation_generator(
                    survey.farmer_id, "long_term_lacks"
                )
                short_term_lacks = self.get_sliced_relation_generator(
                    survey.farmer_id, "short_term_lacks"
                )
                lacks = self.get_sliced_relation_generator(survey.farmer_id, "lacks")
                refuses = self.get_sliced_relation_generator(
                    survey.farmer_id, "subsidy__refuses"
                )

                max_iter_count = max(
                    self.relation_count_mapping[survey.farmer_id].values()
                )

                for i in range(max_iter_count):
                    block1_ = (
                        block1 if i == 0 else [block1[0]] + [""] * (len(block1) - 1)
                    )
                    block2_ = block2 if i == 0 else [""] * len(block2)
                    block3_ = block3 if i == 0 else [""] * len(block3)
                    block4_ = block4 if i == 0 else [""] * len(block4)
                    block5_ = block5 if i == 0 else [""] * len(block5)
                    row = (
                        block1_
                        + list(next(land_areas))
                        + list(next(businesses))
                        + list(next(management_types))
                        + list(next(crop_marketings))
                        + list(next(livestock_marketings))
                        + list(next(annual_incomes))
                        + block2_
                        + list(next(population_ages))
                        + list(next(populations))
                        + block3_
                        + list(next(long_term_hires))
                        + list(next(short_term_hires))
                        + list(next(no_salary_hires))
                        + list(next(lacks))
                        + list(next(long_term_lacks))
                        + list(next(short_term_lacks))
                        + block4_
                        + list(next(refuses))
                        + block5_
                    )
                    yield [output_formatter(item) for item in row]
            except Exception as e:
                print(e)
                errors.append(survey.farmer_id)
        if errors:
            yield ["未匯出成功的調查表：", ",".join(errors)]
        if not self.check_exhausted():
            yield ["匯出錯誤：", "匯出的調查表不完整"]
