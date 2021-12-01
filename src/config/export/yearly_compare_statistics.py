import os
import pandas
from django.db.models import Sum, Count
from django.conf import settings
from openpyxl import load_workbook

from .statistics import StatisticsQueryHelper106, StatisticsQueryHelper107, StatisticsQueryHelper108


class YearlyCompareStatisticsExporter:
    helper_map = {
        106: StatisticsQueryHelper106,
        107: StatisticsQueryHelper107,
        108: StatisticsQueryHelper108
    }

    def __init__(self, y1, y2):
        template = os.path.join(settings.BASE_DIR, 'config/export/templates/statistics_yearly_compare.xlsx')
        self.wb = load_workbook(filename=template)
        self.sheet1 = self.wb['有僱有缺(發布版)比較']
        self.sheet2 = self.wb['有僱有缺(對內版)比較']
        self.sheet3 = self.wb['5-6表(發布)比較']
        self.sheet4 = self.wb['11-14表(對內)比較']
        self.y1 = y1
        self.y2 = y2
        self.y1_helper = self.helper_map.get(y1)()
        self.y1_helper.year = y1
        self.y2_helper = self.helper_map.get(y2)()
        self.y2_helper.year = y2

    def get_sheet_1_3_rows(self, sheet_idx, farmer_id, helper):
        mapping = {
            1: [7, 8, 10, 11, 12, 13],
            3: [7, 8, 10, 11, 12, 13]
        }
        add_target_rows = []
        rows = mapping.get(sheet_idx)

        survey = helper.survey_map.get(farmer_id)
        product_type = survey.management_types.first().type
        region = helper.get_region(survey)

        if product_type == 1:
            add_target_rows.append(rows[0])
        elif product_type == 2:
            add_target_rows.append(rows[1])

        if region == 1:
            add_target_rows.append(rows[2])
        elif region == 2:
            add_target_rows.append(rows[3])
        elif region == 3:
            add_target_rows.append(rows[4])
        elif region == 4:
            add_target_rows.append(rows[5])

        return add_target_rows

    def get_sheet_2_4_rows(self, sheet_idx, farmer_id, helper):
        yearly_crop_mapping = {
            106: {1: 7, 2: 8, 3: 10, 4: 9, 5: 11, 6: 12, 7: 14, 8: 13, 9: 15, 10: 15},
            107: {1: 7, 2: 8, 3: 10, 4: 9, 5: 11, 6: 12, 7: 14, 8: 13, 9: 15, 10: 15},
            108: {1: 7, 2: 8, 3: 10, 4: 9, 5: 11, 6: 12, 7: 13, 8: 15, 9: 15, 10: 14},
        }
        survey = helper.survey_map.get(farmer_id)
        management_type = survey.management_types.first()
        crop_mapping = yearly_crop_mapping.get(helper.year)
        animal_mapping = {11: 17, 12: 18, 13: 19, 14: 20}
        if management_type.id in crop_mapping.keys():
            rows = [6, crop_mapping.get(management_type.id)]
        elif management_type.id in animal_mapping.keys():
            rows = [16, animal_mapping.get(management_type.id)]
        else:
            rows = []
        return rows

    def process_title(self):
        title_mapping = {
            f'{self.y1}年': (['B3', 'D3'], ['D3'], ['B3', 'D3'], ['D3']),
            f'{self.y2}年': (['C3', 'F3'], ['F3'], ['C3', 'H3'], ['H3']),
            f'{self.y1}年較{self.y2}年增減': (['H3'], ['H3'], ['L3'], ['L3'])
        }
        for title, (sheet1_columns, sheet2_columns, sheet3_columns, sheet4_columns) in title_mapping.items():
            for column in sheet1_columns:
                self.sheet1[column] = title
            for column in sheet2_columns:
                self.sheet2[column] = title
            for column in sheet3_columns:
                self.sheet3[column] = title
            for column in sheet4_columns:
                self.sheet4[column] = title

    def process_total(self):
        """Modify sheet 1 column B, C; sheet 2 column B, C; sheet 3 column B, C; sheet4 column B, C"""
        for farmer_id, factor in self.y1_helper.magnification_factor_map.items():
            for row in self.get_sheet_1_3_rows(1, farmer_id, self.y1_helper):
                cell_value = self.sheet1[f'B{row}'].value or 0
                self.sheet1[f'B{row}'] = cell_value + 1 * factor
            for row in self.get_sheet_1_3_rows(3, farmer_id, self.y1_helper):
                cell_value = self.sheet3[f'B{row}'].value or 0
                self.sheet3[f'B{row}'] = cell_value + 1 * factor
            for row in self.get_sheet_2_4_rows(2, farmer_id, self.y1_helper):
                cell_value = self.sheet2[f'B{row}'].value or 0
                self.sheet2[f'B{row}'] = cell_value + 1 * factor
            for row in self.get_sheet_2_4_rows(4, farmer_id, self.y1_helper):
                cell_value = self.sheet4[f'B{row}'].value or 0
                self.sheet4[f'B{row}'] = cell_value + 1 * factor
        # Region cells only
        for farmer_id, factor in self.y2_helper.magnification_factor_map.items():
            for row in self.get_sheet_1_3_rows(1, farmer_id, self.y2_helper)[1:]:  # only use region related row
                cell_value = self.sheet1[f'C{row}'].value or 0
                self.sheet1[f'C{row}'] = cell_value + 1 * factor
            for row in self.get_sheet_1_3_rows(3, farmer_id, self.y2_helper)[1:]:  # only use region related row
                cell_value = self.sheet3[f'C{row}'].value or 0
                self.sheet3[f'C{row}'] = cell_value + 1 * factor

    def process_is_hire(self):
        """Modify sheet 1 column D; sheet 2 column F"""
        mapping = {
            self.y1_helper: 'D',
            self.y2_helper: 'F'
        }
        for helper, column in mapping.items():
            for farmer_id, factor in helper.magnification_factor_map.items():
                survey = helper.survey_map.get(farmer_id)
                if survey.hire:
                    for row in self.get_sheet_1_3_rows(1, farmer_id, helper):
                        cell_value = self.sheet1[f'{column}{row}'].value or 0
                        self.sheet1[f'{column}{row}'] = cell_value + 1 * factor
                    for row in self.get_sheet_2_4_rows(2, farmer_id, helper):
                        cell_value = self.sheet2[f'{column}{row}'].value or 0
                        self.sheet2[f'{column}{row}'] = cell_value + 1 * factor

    def process_is_lack(self):
        """Modify sheet 1 column E; sheet 2 column G"""
        mapping = {
            self.y1_helper: 'E',
            self.y2_helper: 'G'
        }
        for helper, column in mapping.items():
            for farmer_id, factor in helper.magnification_factor_map.items():
                survey = helper.survey_map.get(farmer_id)
                lack = survey.lacks.first()
                if lack.is_lack:
                    for row in self.get_sheet_1_3_rows(1, farmer_id, helper):
                        cell_value = self.sheet1[f'{column}{row}'].value or 0
                        self.sheet1[f'{column}{row}'] = cell_value + 1 * factor
                    for row in self.get_sheet_2_4_rows(2, farmer_id, helper):
                        cell_value = self.sheet2[f'{column}{row}'].value or 0
                        self.sheet2[f'{column}{row}'] = cell_value + 1 * factor

    def process_long_term_hires(self):
        """Modify sheet 3 column D, E, H, I; sheet 4 column D, E, H, I"""
        helper_mapping = {
            self.y1_helper: 'DE',
            self.y2_helper: 'HI',
        }
        for helper, (column1, column2) in helper_mapping.items():
            qs = helper.survey_qs.prefetch_related(
                'long_term_hires', 'long_term_hires__number_workers',
            ).values('farmer_id').annotate(
                sum_workers=Sum('long_term_hires__number_workers__count'),
            )
            for result in qs:
                farmer_id = result['farmer_id']
                factor = helper.magnification_factor_map[farmer_id]
                sum_workers = result['sum_workers'] * factor if result['sum_workers'] else 0
                if sum_workers:
                    for row in self.get_sheet_1_3_rows(3, farmer_id, helper):
                        cell_value = self.sheet3[f'{column1}{row}'].value or 0
                        self.sheet3[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet3[f'{column2}{row}'].value or 0
                        self.sheet3[f'{column2}{row}'] = cell_value + sum_workers
                    for row in self.get_sheet_2_4_rows(4, farmer_id, helper):
                        cell_value = self.sheet4[f'{column1}{row}'].value or 0
                        self.sheet4[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet4[f'{column2}{row}'].value or 0
                        self.sheet4[f'{column2}{row}'] = cell_value + sum_workers

    def process_long_term_lacks(self):
        """Modify sheet 3 column F, G, J, K; sheet 4 column F, G, J, K"""
        helper_mapping = {
            self.y1_helper: 'FG',
            self.y2_helper: 'JK',
        }
        for helper, (column1, column2) in helper_mapping.items():
            qs = helper.survey_qs.prefetch_related(
                'long_term_lacks',
            ).filter(farmer_id__in=helper.lack_farmer_ids).values('farmer_id').annotate(
                sum_workers=Sum('long_term_lacks__count'),
            )
            for result in qs:
                farmer_id = result['farmer_id']
                factor = helper.magnification_factor_map[farmer_id]
                sum_workers = result['sum_workers'] * factor if result['sum_workers'] else 0
                if sum_workers:
                    for row in self.get_sheet_1_3_rows(3, farmer_id, helper):
                        cell_value = self.sheet3[f'{column1}{row}'].value or 0
                        self.sheet3[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet3[f'{column2}{row}'].value or 0
                        self.sheet3[f'{column2}{row}'] = cell_value + sum_workers
                    for row in self.get_sheet_2_4_rows(4, farmer_id, helper):
                        cell_value = self.sheet4[f'{column1}{row}'].value or 0
                        self.sheet4[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet4[f'{column2}{row}'].value or 0
                        self.sheet4[f'{column2}{row}'] = cell_value + sum_workers

    def process_short_term_hires(self):
        """Modify sheet 3 column D, E, H, I; sheet 4 column D, E, H, I"""
        helper_mapping = {
            self.y1_helper: 'DE',
            self.y2_helper: 'HI',
        }
        for helper, (column1, column2) in helper_mapping.items():
            qs = helper.survey_qs.prefetch_related(
                'short_term_hires', 'short_term_hires__number_workers',
            ).values('farmer_id').annotate(
                sum_workers=Sum('short_term_hires__number_workers__count'),
            )
            for result in qs:
                farmer_id = result['farmer_id']
                factor = helper.magnification_factor_map[farmer_id]
                sum_workers = result['sum_workers'] * factor if result['sum_workers'] else 0
                if sum_workers:
                    # The target is the third table in the sheet
                    for row in [i + 27 for i in self.get_sheet_1_3_rows(3, farmer_id, helper)]:
                        cell_value = self.sheet3[f'{column1}{row}'].value or 0
                        self.sheet3[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet3[f'{column2}{row}'].value or 0
                        self.sheet3[f'{column2}{row}'] = cell_value + sum_workers
                    for row in [i + 41 for i in self.get_sheet_2_4_rows(4, farmer_id, helper)]:
                        cell_value = self.sheet4[f'{column1}{row}'].value or 0
                        self.sheet4[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet4[f'{column2}{row}'].value or 0
                        self.sheet4[f'{column2}{row}'] = cell_value + sum_workers

    def process_short_term_lacks(self):
        """Modify sheet 3 column F, G, J, K; sheet 4 column F, G, J, K"""
        helper_mapping = {
            self.y1_helper: 'FG',
            self.y2_helper: 'JK',
        }
        for helper, (column1, column2) in helper_mapping.items():
            qs = helper.survey_qs.prefetch_related(
                'short_term_lacks',
            ).filter(farmer_id__in=helper.lack_farmer_ids).values('farmer_id', 'short_term_lacks__count').annotate(
                month_count=Count('short_term_lacks__months'),
            ).filter(month_count__gte=1)

            df = pandas.DataFrame(list(qs))
            df['workers'] = df['short_term_lacks__count'] * df['month_count']
            df = df.groupby('farmer_id', as_index=False).agg({'workers': 'sum'})

            for _, result in df.iterrows():
                farmer_id = result['farmer_id']
                factor = helper.magnification_factor_map[farmer_id]
                sum_workers = result['workers'] * factor if result['workers'] else 0
                if sum_workers:
                    # The target is the third table in the sheet
                    for row in [i + 27 for i in self.get_sheet_1_3_rows(3, farmer_id, helper)]:
                        cell_value = self.sheet3[f'{column1}{row}'].value or 0
                        self.sheet3[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet3[f'{column2}{row}'].value or 0
                        self.sheet3[f'{column2}{row}'] = cell_value + sum_workers
                    for row in [i + 41 for i in self.get_sheet_2_4_rows(4, farmer_id, helper)]:
                        cell_value = self.sheet4[f'{column1}{row}'].value or 0
                        self.sheet4[f'{column1}{row}'] = cell_value + 1 * factor
                        cell_value = self.sheet4[f'{column2}{row}'].value or 0
                        self.sheet4[f'{column2}{row}'] = cell_value + sum_workers


    def __call__(self, *args, **kwargs):
        self.process_title()
        self.process_total()
        self.process_is_hire()
        self.process_long_term_hires()
        self.process_short_term_hires()
        self.process_is_lack()
        self.process_long_term_lacks()
        self.process_short_term_lacks()
        self.wb.save(*args, **kwargs)
