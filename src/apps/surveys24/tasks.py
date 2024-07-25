from config import celery_app as app
from apps.surveys24.models import FarmerStat, Survey


@app.task
def async_update_stratify(survey_id):
    survey = Survey.objects.get(id=survey_id)
    if "無效戶" in survey.note:
        FarmerStat.objects.filter(survey=survey).delete()
        return f"Delete {survey} FarmerStat, it's been mark as invalid farmer."
    else:
        is_senility = FarmerStat.get_is_senility(survey)
        stratify = FarmerStat.get_stratify(survey, is_senility)
        FarmerStat.objects.update_or_create(
            survey=survey, defaults={"stratify": stratify}
        )
        return f"Classify survey {survey} to stratify {stratify}."
