import logging
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.exceptions import (
    ValidationError,
)
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import BuilderFileSerializer
from apps.surveys18.models import BuilderFile

system_logger = logging.getLogger('system')


class BuilderFileCreateAPIView(CreateAPIView):
    queryset = BuilderFile.objects.all()
    serializer_class = BuilderFileSerializer
    # permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                datafile = self.request.data.get('datafile')
                token = self.request.data.get('token')
                user = self.request.user
                if not isinstance(user, User):
                    user = None

                serializer.save(user=user,
                                datafile=datafile, token=token)
        except Exception as e:
            system_logger.exception(e)
            raise ValidationError(e)
