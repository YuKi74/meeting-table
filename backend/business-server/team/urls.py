from django.urls import path

from .views import (ApplicationView, TeamInformationView, TeamMemberQuitView,
                    TeamMemberView, TeamView)

urlpatterns = [
    path('', TeamView.as_view()),  # 4
    path('join/', ApplicationView.as_view()),  # 2
    path('member/', TeamMemberView.as_view()),  # 3
    path('quit/', TeamMemberQuitView.as_view()),  # 1
    path('<str:uuid>/', TeamInformationView.as_view()),
]
