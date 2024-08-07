# api/serializers.py
from rest_framework import serializers
from .models import QRCodeReading

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeReading
        fields = ['qrcode_data']
