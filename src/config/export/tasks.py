import os
import csv
import pyminizip
import traceback
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

from config import celery_app as app
from . import (
    full_data,
    statistics,
    yearly_compare_statistics,
    examinations,
    raw_data,
    farmer_stat,
)


@app.task
def async_export_full_data(year, email):
    factory_map = {
        107: full_data.SurveyRelationGeneratorFactory107,
        108: full_data.SurveyRelationGeneratorFactory108,
        110: full_data.SurveyRelationGeneratorFactory110,
        111: full_data.SurveyRelationGeneratorFactory111,
    }
    try:
        factory = factory_map.get(year)(excludes={"note__icontains": "無效戶"})
        row_generator = factory.export_generator()

        file_name = f"{year}_Full_Export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        csv_path = f"{file_name}.csv"
        zip_path = f"{file_name}.zip"

        with open(csv_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for row in row_generator:
                writer.writerow(row)

        password = get_random_string(length=24)
        pyminizip.compress(csv_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{year}調查表匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{year}調查表.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{year}調查表匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
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
        106: statistics.StatisticsExporter106,
        107: statistics.StatisticsExporter107,
        108: statistics.StatisticsExporter108,
        110: statistics.StatisticsExporter110,
        111: statistics.StatisticsExporter111,
    }
    try:
        exporter = exporter_map.get(year)()
        file_name = (
            f"{year}_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )

        file_path = f"{file_name}.xlsx"
        zip_path = f"{file_name}.zip"

        exporter(file_path)

        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{year}平台統計結果表式匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{year}平台統計結果表式.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{year}平台統計結果表式匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
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
        exporter = yearly_compare_statistics.YearlyCompareStatisticsExporter(y1, y2)

        file_name = f"{y1}_{y2}_Compare_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        file_path = f"{file_name}.xlsx"
        zip_path = f"{file_name}.zip"

        exporter(file_path)

        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{y1}-{y2}年結果表匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{y1}-{y2}年結果表.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{y1}-{y2}年結果表匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass


@app.task
def async_export_examination_work_hours(year, email):
    import apps.surveys19.models
    import apps.surveys20.models
    import apps.surveys22.models
    import apps.surveys23.models
    import apps.surveys24.models

    models_map = {
        107: apps.surveys19.models,
        108: apps.surveys20.models,
        110: apps.surveys22.models,
        111: apps.surveys23.models,
        112: apps.surveys24.models
    }
    try:
        models = models_map.get(year)
        if year < 111:
            exporter = examinations.WorkHourExaminationExporterV1
        else:
            exporter = examinations.WorkHourExaminationExporterV2
        row_generator = exporter(models.Survey, models.Product)()

        file_name = f"{year}_WorkHour_Examination_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        csv_path = f"{file_name}.csv"
        zip_path = f"{file_name}.zip"

        with open(csv_path, "w+", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for row in row_generator:
                writer.writerow(row)

        password = get_random_string(length=24)
        pyminizip.compress(csv_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{year}工時檢誤匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{year}工時檢誤.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{year}工時檢誤匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        ).send()
    finally:
        try:
            os.remove(csv_path)
            os.remove(zip_path)
        except Exception:
            pass


@app.task
def async_export_raw_data(year, email):
    exporter_map = {
        110: raw_data.RawDataExporter110,
        111: raw_data.RawDataExporter111,
    }
    try:
        exporter = exporter_map.get(year)()
        file_name = (
            f"{year}_RawData_Export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )
        file_path = f"{file_name}.xlsx"
        zip_path = f"{file_name}.zip"

        exporter(file_path)
        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{year}原始資料匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{year}原始資料.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{year}原始資料匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass


@app.task
def async_export_farmer_stat(year, email):
    exporter_map = {
        110: farmer_stat.FarmerStatExporter110,
        111: farmer_stat.FarmerStatExporter111,
        112: farmer_stat.FarmerStatExporter112,
    }
    try:
        exporter = exporter_map.get(year)()
        file_name = (
            f"{year}_FarmerStat_Export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )
        file_path = f"{file_name}.xlsx"
        zip_path = f"{file_name}.zip"

        exporter(file_path, sheet_name="農戶統計")
        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, "rb") as zip_file:
            mail = EmailMessage(
                f"{year}農戶統計匯出完成",
                f"匯出結果如附件，解壓縮密碼請輸入：{password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            mail.attach(f"{year}農戶統計.zip", zip_file.read(), "application/zip")
            mail.send()
    except Exception as e:
        EmailMessage(
            f"{year}農戶統計匯出失敗",
            f"系統發生錯誤，請通知管理員處理。\n{traceback.format_exc()}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        ).send()
    finally:
        try:
            os.remove(file_path)
            os.remove(zip_path)
        except Exception:
            pass
