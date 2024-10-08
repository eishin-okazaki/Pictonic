from django.db import models
from django.contrib.auth import get_user_model
from .generated_image_model import GeneratedImage

User = get_user_model()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    image = models.ForeignKey(GeneratedImage, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark {self.id} by {self.user.email}"
