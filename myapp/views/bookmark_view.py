from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from myapp.models import GeneratedImage, Bookmark
from django.urls import reverse

@login_required
def bookmark_view(request, image_id):
    try:
        image = GeneratedImage.objects.get(id=image_id)
        Bookmark.objects.get_or_create(user=request.user, image=image)
        redirect_url = f"{reverse('summarizer')}?image_id={image_id}"
        return redirect(redirect_url)
    except GeneratedImage.DoesNotExist:
        return redirect('summarizer')
