from rest_framework import serializers
from ..models import PatientHistory

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = "__all__"