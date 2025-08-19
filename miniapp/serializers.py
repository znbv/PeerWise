from rest_framework import serializers
from miniapp.models import Tutor

class tutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'