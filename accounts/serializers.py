from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:   
        model = User
        fields = '__all__'

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('There is no user registered with this email address.')
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            password = make_password(validated_data['password'])
        )
        return user
    