from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserRankinSerializer
from qranalizer.models import QRCodeReading
from django.db.models import Count

class RankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = User.objects.annotate(points=Count('qrcodereading')).order_by('-points')
        serializer = UserRankinSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
