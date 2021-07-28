from .views import UserView, UserRegisterView, UserLoginView, UserEditView
from django.urls import path, include, re_path

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('user_info/<int:pk>/', UserView.as_view()),
    path('edit_user_info/', UserEditView.as_view())
]
