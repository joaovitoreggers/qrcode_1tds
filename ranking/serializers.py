from django.contrib.auth.models import User
from rest_framework import serializers

class UserRankinSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'points']