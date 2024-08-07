from django.db import models
from django.contrib.auth.models import User

class QRCodeReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qrcode_data = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'qrcode_data')

    def __str__(self):
        return f'{self.user.username} - self.qr_code_data'