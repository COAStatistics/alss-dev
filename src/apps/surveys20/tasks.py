import csv
import io

from django.conf import settings
from django.core.mail import EmailMessage

from config import celery_app as app
from apps.surveys20.models import FarmerStat, Survey
from apps.surveys20.export import SurveyRelationGeneratorFactory


@app.task
def async_export_108(email):
    try:
        factory = SurveyRelationGeneratorFactory(excludes={'note__icontains': '無效戶'})
        row_generator = factory.export_generator()

        sio = io.StringIO()
        writer = csv.writer(sio)

        for row in row_generator:
            writer.writerow(row)

        email = EmailMessage(
            '108調查表匯出完成',
            '請下載附件後解壓縮查看調查表',
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        email.attach('108調查表.csv', sio.getvalue(), 'text/csv')
        email.send()
    except Exception as e:
        email = EmailMessage(
            '108調查表匯出失敗',
            f"系統發生錯誤，請通知管理員處理。\n{e}",
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )
        email.send()


@app.task
def async_update_stratify(survey_id):
    survey = Survey.objects.get(id=survey_id)
    stratify = FarmerStat.get_stratify(survey)
    FarmerStat.objects.update_or_create(
        survey=survey,
        defaults={
            'stratify': stratify
        }
    )

    return f'Classify survey {survey} to stratify {stratify}.'
