from django.db import models
from django.conf import settings
from django.utils.timezone import now

class UserImage(models.Model):
    img_path = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        (1, 'オリジナル画像'),
        (2, '生成画像'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    STATUS_CHOICES = (
        (1, 'アクティブ'),
        (2, '非アクティブ'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.img_path
