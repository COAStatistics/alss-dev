import json
import logging
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated

from .serializers import ReviewLogSerializer, ReviewLogListSerializer, ReviewLogUpdateSerializer

from apps.logs.models import ReviewLog, query_by_args

logger = logging.getLogger("review")


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
