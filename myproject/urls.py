from django.contrib import admin
from django.urls import path
from myapp.views import login_view,user_register_view,summarizer_view,mypage_view,bookmark_view
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('user_register/', user_register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('summarizer/', summarizer_view, name='summarizer'),
    path('mypage/', mypage_view, name='mypage'),
    path('bookmark_image/<int:image_id>/', bookmark_view, name='bookmark_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
