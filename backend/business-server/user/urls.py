from .views import UserView, UserRegisterView, UserLoginView, UserEditView
from django.urls import path, include, re_path

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegisterView.as_view()),
    # 查看其他用户的信息get
    path('<int:id>/', UserView.as_view()),
    # 查看用户自己的个人信息get，更新个人信息patch
    path('', UserEditView.as_view()),
]
