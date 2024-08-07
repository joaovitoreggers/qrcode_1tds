# api/views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import QRCodeReading
from .serializers import QRCodeSerializer
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import io

class QRCodeReader(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'Image file not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image = request.FILES['image']
        image_np = np.frombuffer(image.read(), np.uint8)
        image_pil = Image.open(io.BytesIO(image_np))
        
        decoded_objects = decode(image_pil)
        
        if decoded_objects:
            data = decoded_objects[0].data.decode('utf-8')
            print(f"Dados do QR code decodificados: {data}")
            serializer = QRCodeSerializer(data={'qrcode_data': data})
            if serializer.is_valid():
                qr_code_reading, created = QRCodeReading.objects.get_or_create(
                    user=request.user,
                    qrcode_data=data
                )
                if created:
                    return Response({'data': data, 'message': 'QR code lido com sucesso e ponto adicionado'}, status=status.HTTP_200_OK)
                else:
                    return Response({'data': data, 'message': 'QR code already read'}, status=status.HTTP_200_OK)
            else:
                print(f"Erros de validação do serializer: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Nenhum QR code encontrado na imagem.")
            return Response({'error': 'No QR code found'}, status=status.HTTP_400_BAD_REQUEST)
