import json
import logging
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.generics import (
    UpdateAPIView,
    ListAPIView,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from .serializers import (
    ReviewLogListSerializer,
    ReviewLogUpdateSerializer,
)

from . import serializers_singleton

from logs.models import ReviewLog, query_by_args

logger = logging.getLogger('review')


class ReviewLogViewSet(viewsets.ModelViewSet):
    queryset = ReviewLog.objects.all()
    serializer_class = ReviewLogListSerializer
    permission_classes = [IsAuthenticated]

    # overwrite list for jQuery DataTable
    def list(self, request, **kwargs):
        reviews = query_by_args(request, **request.query_params)
        serializer = ReviewLogListSerializer(reviews['items'], many=True)
        result = dict()
        result['data'] = serializer.data
        result['draw'] = reviews['draw']
        result['recordsTotal'] = reviews['total']
        result['recordsFiltered'] = reviews['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


class ReviewLogUpdateAPIView(UpdateAPIView):
    queryset = ReviewLog.objects.all()
    serializer_class = ReviewLogUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, user, object_id, content_type):
        return ReviewLog.objects.filter(user=user, object_id=object_id, content_type=content_type).first()

    def patch(self, request):
        data = json.loads(request.data.get('data'))
        object_id = data.get('object_id')
        app_label = data.get('app_label')
        model = data.get('model')
        data['user'] = request.user.id
        content_type = ContentType.objects.filter(app_label=app_label, model=model).first()
        data['content_type'] = content_type.id
        obj = self.get_object(request.user, object_id, content_type)

        serializer = ReviewLogUpdateSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data)
        else:
            logger.exception(serializer.errors, extra={
                'user': request.user,
                'content_type': content_type,
                'object_id': object_id,
            })
            return JsonResponse(data=serializer.errors, safe=False)


class ReviewLogSingletonListAPIView(ListAPIView):
    serializer_class = serializers_singleton.ReviewLogSerializer
    queryset = ReviewLog.objects.all()
    permission_classes = [IsAuthenticated]
