# myapp/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_images')
    summary_text = models.TextField(null=True)
    image = models.ImageField(upload_to='generated_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} by {self.user.email}"
