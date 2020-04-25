import json
import logging
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from model_utils import Choices
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from config.permissions import IsSuperUser
from apps.logs.models import ReviewLog
from .serializers import ReviewLogSerializer, ReviewLogListSerializer, ReviewLogUpdateSerializer


logger = logging.getLogger("review")


ORDER_COLUMN_CHOICES = Choices(
    ("0", "id"),
    ("1", "user"),
    ("2", "content_object"),
    ("3", "current_errors"),
    ("4", "update_time"),
)


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
        if app_label == 'surveys20':
            queryset = queryset.filter(
                Q(surveys20__farmer_id__icontains=search_value)
                | Q(user__full_name__icontains=search_value)
                | Q(user__email__icontains=search_value)
            )

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start: start + length]
    return {"items": queryset, "count": count, "total": total, "draw": draw}


class ReviewLogViewSet(viewsets.ModelViewSet):
    queryset = ReviewLog.objects.all()
    serializer_class = ReviewLogListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ReviewLogUpdateSerializer
        if self.action == 'list':
            return ReviewLogListSerializer
        return ReviewLogSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def datatable(self, request):
        result = dict()
        params = request.query_params
        if params:
            reviews = query_by_args(request, **params)
            if reviews:
                serializer = ReviewLogListSerializer(reviews["items"], many=True)
                result["data"] = serializer.data
                result["draw"] = reviews.get("draw")
                result["recordsTotal"] = reviews.get("total")
                result["recordsFiltered"] = reviews.get("count")
        return Response(
            result, status=status.HTTP_200_OK, template_name=None, content_type=None
        )

    def patch(self, request):
        data = json.loads(request.data.get("data"))
        object_id = data.get("object_id")
        app_label = data.get("app_label")
        model = data.get("model")
        data["user"] = request.user.id
        content_type = ContentType.objects.filter(
            app_label=app_label, model=model
        ).first()
        data["content_type"] = content_type.id
        obj = ReviewLog.objects.filter(user=request.user, object_id=object_id, content_type=content_type).first()

        serializer = ReviewLogUpdateSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data)
        else:
            logger.exception(
                serializer.errors,
                extra={
                    "user": request.user,
                    "content_type": content_type,
                    "object_id": object_id,
                },
            )
            return JsonResponse(data=serializer.errors, safe=False)
