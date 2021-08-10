from django.urls import path

from .views import (ApplicationView, MeetingRoomView, TeamInformationView,
                    TeamMeetingRoomView, TeamMemberQuitView, TeamMemberView,
                    TeamView, FileTransferView, FileView, VideoTokenView)

urlpatterns = [
    path('', TeamView.as_view()),
    path('join/', ApplicationView.as_view()),
    path('member/', TeamMemberView.as_view()),
    path('member/<int:member_id>/', TeamMemberView.as_view()),
    path('quit/', TeamMemberQuitView.as_view()),
    path('room/', MeetingRoomView.as_view()),
    path('room/<int:room_id>/', MeetingRoomView.as_view()),
    path('room/<str:uuid>/', MeetingRoomView.as_view()),
    path('rooms/', TeamMeetingRoomView.as_view()),
    path('file/', FileTransferView.as_view()),
    path('file/<int:record_id>/', FileTransferView.as_view()),
    path('file/<str:uuid>/', FileView.as_view()),
    path('<str:uuid>/', TeamInformationView.as_view()),
    path('video_token/<str:room_uuid>/', VideoTokenView.as_view())
]
