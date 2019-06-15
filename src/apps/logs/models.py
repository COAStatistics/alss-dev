from django.db.models import (
    Model,
    IntegerField,
    PositiveIntegerField,
    ForeignKey,
    DateTimeField,
    CASCADE,
    Q,
)
from model_utils import Choices
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

SURVEY_CHOICES = Q(app_label="surveys18", model="survey") | Q(app_label="surveys19", model="survey")

ORDER_COLUMN_CHOICES = Choices(
    ("0", "id"),
    ("1", "user"),
    ("2", "content_object"),
    ("3", "current_errors"),
    ("4", "update_datetime"),
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
    update_datetime = DateTimeField(
        auto_now=True,
        auto_now_add=False,
        null=True,
        blank=True,
        verbose_name=_("Updated"),
    )

    class Meta:
        verbose_name = _("ReviewLog")
        verbose_name_plural = _("ReviewLogs")


def query_by_args(request, **kwargs):
    app_label = kwargs.get("app_label")[0]
    draw = int(kwargs.get("draw")[0])
    length = int(kwargs.get("length")[0])
    start = int(kwargs.get("start")[0])
    order_column = kwargs.get("order[0][column]")[0]
    order = kwargs.get("order[0][dir]")[0]
    search_value = kwargs.get("search[value]")[0]

    order_column = ORDER_COLUMN_CHOICES[order_column]
    # django orm '-' -> desc
    if order == "desc":
        order_column = "-" + order_column

    if request.user.is_staff:
        queryset = ReviewLog.objects.all()
    else:
        queryset = ReviewLog.objects.filter(user=request.user).all()

    if app_label:
        queryset = queryset.filter(content_type__app_label=app_label)

    total = queryset.count()

    if search_value:
        if app_label == 'surveys18':
            queryset = queryset.filter(
                Q(surveys18__farmer_id__icontains=search_value)
                | Q(user__full_name__icontains=search_value)
                | Q(user__email__icontains=search_value)
            )
        if app_label == 'surveys19':
            queryset = queryset.filter(
                Q(surveys19__farmer_id__icontains=search_value)
                | Q(user__full_name__icontains=search_value)
                | Q(user__email__icontains=search_value)
            )

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start: start + length]
    return {"items": queryset, "count": count, "total": total, "draw": draw}
