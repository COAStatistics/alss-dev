import os
import csv
import pyminizip
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

from config import celery_app as app
from .yearly_compare_statistics import YearlyCompareStatisticsExporter
from .statistics import StatisticsExporter106, StatisticsExporter107, StatisticsExporter108
from .full_data import SurveyRelationGeneratorFactory107, SurveyRelationGeneratorFactory108

@app.task
def async_export_full_data(year, email):
    factory_map = {
        107: SurveyRelationGeneratorFactory107,
        108: SurveyRelationGeneratorFactory108
    }
    try:
        factory = factory_map.get(year)(excludes={'note__icontains': '無效戶'})
        row_generator = factory.export_generator()

        file_name = f"{year}_Full_Export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        csv_path = f'{file_name}.csv'
        zip_path = f'{file_name}.zip'

        with open(csv_path, 'w+', encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in row_generator:
                writer.writerow(row)

        password = get_random_string(length=24)
        pyminizip.compress(csv_path, "", zip_path, password, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                f'{year}調查表匯出完成',
                f'匯出結果如附件，解壓縮密碼請輸入：{password}',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach(f'{year}調查表.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            f'{year}調查表匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
    finally:
        try:
            os.remove(csv_path)
            os.remove(zip_path)
        except Exception:
            pass

@app.task
def async_export_statistics(year, email):
    exporter_map = {
        106: StatisticsExporter106,
        107: StatisticsExporter107,
        108: StatisticsExporter108,
    }
    try:
        exporter = exporter_map.get(year)()
        file_name = f"{year}_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        file_path = f'{file_name}.xlsx'
        zip_path = f'{file_name}.zip'

        exporter(file_path)

        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                f'{year}平台統計結果表式匯出完成',
                f'匯出結果如附件，解壓縮密碼請輸入：{password}',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach(f'{year}平台統計結果表式.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            f'{year}平台統計結果表式匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass

@app.task
def async_export_yearly_compare_statistics(y1, y2, email):
    try:
        exporter = YearlyCompareStatisticsExporter(y1, y2)

        file_name = f"{y1}_{y2}_Compare_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        file_path = f'{file_name}.xlsx'
        zip_path = f'{file_name}.zip'

        exporter(file_path)

        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                f'{y1}-{y2}年結果表匯出完成',
                f'匯出結果如附件，解壓縮密碼請輸入：{password}',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach(f'{y1}-{y2}年結果表.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            f'{y1}-{y2}年結果表匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass
