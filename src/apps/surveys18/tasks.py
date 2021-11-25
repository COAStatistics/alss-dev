import os
import csv
import pyminizip
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

from config import celery_app as app
from apps.surveys18.models import FarmerStat, Survey
from apps.surveys18.export import StatisticsExporter


@app.task
def async_export_106_statistics(email):
    try:
        exporter = StatisticsExporter()

        file_name = f"106_Statistic_Report_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        file_path = f'{file_name}.xlsx'
        zip_path = f'{file_name}.zip'

        exporter(file_path)

        password = get_random_string(length=24)
        pyminizip.compress(file_path, "", zip_path, password, 5)

        with open(zip_path, 'rb') as zip_file:
            mail = EmailMessage(
                '106平台統計結果表式匯出完成',
                f'匯出結果如附件，解壓縮密碼請輸入：{password}',
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            mail.attach('106平台統計結果表式.zip', zip_file.read(), 'application/zip')
            mail.send()
    except Exception as e:
        EmailMessage(
            '106平台統計結果表式匯出失敗',
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
