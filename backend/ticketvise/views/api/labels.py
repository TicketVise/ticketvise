from rest_framework.serializers import ModelSerializer

from ticketvise.models.label import Label


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ["name", "color", "id"]
