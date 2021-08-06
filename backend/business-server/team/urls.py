from django.urls import path

from .views import (ApplicationView, FileTransferView, FileView,
                    MeetingRoomView, TeamInformationView, TeamMeetingRoomView,
                    TeamMemberQuitView, TeamMemberView, TeamView)

urlpatterns = [
    path('', TeamView.as_view()),
    path('join/', ApplicationView.as_view()),
    path('member/', TeamMemberView.as_view()),
    path('member/<int:member_id>/', TeamMemberView.as_view()),
    path('quit/', TeamMemberQuitView.as_view()),
    path('room/', MeetingRoomView.as_view()),
    path('room/<int:id>/', MeetingRoomView.as_view()),
    path('room/<str:uuid>/', MeetingRoomView.as_view()),
    path('rooms/', TeamMeetingRoomView.as_view()),
    path('file/', FileTransferView.as_view()),
    path('file/<int:id>/', FileTransferView.as_view()),
    path('file/<int:id>/', FileView.as_view()),
    path('file/<str:uuid>/', FileView.as_view()),
    path('<str:uuid>/', TeamInformationView.as_view()),

]
