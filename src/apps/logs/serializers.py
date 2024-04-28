from django.utils import timezone
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField,
    RelatedField,
)
from apps.logs.models import ReviewLog
from apps.surveys18.models import Survey as Survey18
from apps.surveys19.models import Survey as Survey19
from apps.surveys20.models import Survey as Survey20
from apps.surveys22.models import Survey as Survey22
from apps.surveys23.models import Survey as Survey23
from apps.surveys24.models import Survey as Survey24


class ContentObjectRelatedField(RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize content objects to a simple textual representation.
        """
        if any(
            isinstance(value, cls)
            for cls in (Survey18, Survey19, Survey20, Survey22, Survey23, Survey24)
        ):
            return value.farmer_id
        raise Exception("Unexpected type of content object")


class ReviewLogListSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    user = SerializerMethodField(read_only=True)
    content_object = ContentObjectRelatedField(read_only=True)
    update_time = SerializerMethodField(read_only=True)

    def get_user(self, instance):
        return instance.user.full_name or instance.user.email

    def get_update_time(self, instance):
        return timezone.localtime(instance.update_time).strftime("%Y/%m/%d %H:%M:%S")

    class Meta:
        model = ReviewLog
        fields = "__all__"


class ReviewLogUpdateSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ReviewLog
        fields = "__all__"

    def create(self, validated_data):
        content_type = validated_data["content_type"]
        object_id = validated_data["object_id"]

        if content_type and object_id:
            obj = (
                ReviewLog.objects.filter(content_type=content_type, object_id=object_id)
                .order_by("update_time")
                .first()
            )
            if obj:
                # get earliest initial errors if already been count
                initial_errors = obj.initial_errors if obj else None
            else:
                initial_errors = (
                    validated_data["initial_errors"]
                    if "initial_errors" in validated_data
                    else None
                )

            current_errors = (
                validated_data["current_errors"]
                if "current_errors" in validated_data
                else None
            )
            exception_errors = (
                validated_data["exception_errors"]
                if "exception_errors" in validated_data
                else 0
            )

            instance = ReviewLog.objects.create(
                user=validated_data["user"],
                content_type=content_type,
                object_id=object_id,
                initial_errors=initial_errors,
                current_errors=current_errors,
                exception_errors=exception_errors,
            )
            return instance

    def update(self, instance, validated_data):
        if "current_errors" in validated_data:
            instance.current_errors = validated_data["current_errors"]
        if "exception_errors" in validated_data:
            instance.exception_errors = validated_data["exception_errors"]
        instance.save()
        return instance


class ReviewLogSerializer(ModelSerializer):
    class Meta:
        model = ReviewLog
        fields = "__all__"
