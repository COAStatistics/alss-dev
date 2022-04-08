from django.db.models import (
    Model,
    IntegerField,
    PositiveIntegerField,
    ForeignKey,
    DateTimeField,
    CASCADE,
    Q,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

SURVEY_CHOICES = (
    Q(app_label="surveys18", model="survey")
    | Q(app_label="surveys19", model="survey")
    | Q(app_label="surveys20", model="survey")
    | Q(app_label="surveys22", model="survey")
)


class ReviewLog(Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=CASCADE,
        related_name="review_logs",
        verbose_name=_("User"),
    )
    content_type = ForeignKey(
        ContentType, limit_choices_to=SURVEY_CHOICES, on_delete=CASCADE
    )
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    initial_errors = IntegerField(
        null=True, blank=True, verbose_name=_("Initialed Error Count")
    )
    current_errors = IntegerField(
        null=True, blank=True, verbose_name=_("Current Error Count")
    )
    exception_errors = IntegerField(
        default=0, verbose_name=_("Exception Error Count")
    )
    update_time = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ReviewLog")
        verbose_name_plural = _("ReviewLogs")
