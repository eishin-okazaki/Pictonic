from .models import UserImage

def user_info(request):
    data = {}
    if request.user.is_authenticated:
        data['login_user_image'] = UserImage.objects.filter(user=request.user).first().img_path if UserImage.objects.filter(user=request.user).exists() else 'default_user_icon.png'
        data['login_user_name'] = request.user.name
        data['login_user_email'] = request.user.email
    return data