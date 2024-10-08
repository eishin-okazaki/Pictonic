from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.models import Bookmark

@login_required
def mypage_view(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'mypage.html', {'bookmarks': bookmarks})
