from rest_framework import serializers
from apps.logs import models


class ReviewLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReviewLog
        fields = '__all__'
