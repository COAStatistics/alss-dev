from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)
from apps.surveys18.models import BuilderFile, BuilderFileType
from apps.surveys18.builder.tokenizer_labor import Builder as LaborBuilder
from apps.surveys18.builder.tokenizer_specialty import Builder as SpecialtyBuilder


class BuilderFileTypeSerializer(ModelSerializer):
    class Meta:
        model = BuilderFileType
        fields = "__all__"


class BuilderFileSerializer(HyperlinkedModelSerializer):
    type = PrimaryKeyRelatedField(queryset=BuilderFileType.objects.all())

    class Meta:
        model = BuilderFile
        fields = ["token", "datafile", "type"]

    def create(self, validated_data):
        return BuilderFile.objects.create(**validated_data)

    def validate(self, data):
        """
        Validate via build
        """
        try:
            errors = list()
            file_type = data.get("type")
            file = data.get("datafile")
            token = data.get("token")
            if token:
                content = [token]

            if file:
                content = file.read().decode("utf-8-sig").splitlines()

            if file and token:
                raise ValidationError(
                    "Not Allow To Provide Upload File And Single Token At Same Time"
                )

            for i, string in enumerate(content):
                try:
                    if file_type.id == 1:
                        builder = LaborBuilder(string=string)

                    elif file_type.id == 2:
                        builder = SpecialtyBuilder(string=string)

                    builder.build()
                    builder.build(readonly=False)

                except Exception as e:
                    errors.append({"string": string, "index": i, "error": e})

            if errors:
                raise ValidationError(errors)
            return data
        except Exception as e:
            raise ValidationError(e)
