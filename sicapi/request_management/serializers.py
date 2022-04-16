from rest_framework import serializers
from .models import InfoAppeal, InfoRequest

class InfoAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoAppeal
        fields = [
            "content",
            "answer",
            "open_date",
            "answer_date"
        ]

class InfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoRequest
        fields = [
            "demander",
            "content",
            "answer",
            "open_date",
            "answer_date",
            "status",
            "appeal"
        ]