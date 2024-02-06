from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RendezVous

from rest_framework import serializers
from django.contrib.auth.models import User

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']
        
class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'