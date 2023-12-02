from rest_framework import serializers
from .models import Process


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'
