from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('get-user/', views.GetUser.as_view(), name='get-user'),
    path('handle-friends/', views.HandleFriends.as_view(), name='handle-friends'),
    path('update-user/', views.UpdateUser.as_view(), name='update-user'),
    path('remove-friend/', views.RemoveFriend.as_view(), name='remove-friend'),
    path('handle-messages/<int:by>/<int:to>/', views.HandleMessages.as_view(), name='handle-messages'),
    path('handle-group/', views.HandleGroup.as_view(), name='handle-group'),
    path('update-group/', views.UpdateGroup.as_view(), name='update-group'),
    path('delete-group/', views.DeleteGroup.as_view(), name='delete-group'),
    path('leave-group/', views.LeaveGroup.as_view(), name='leave-group'),
    path('group-messages/<int:id>/', views.GroupMessages.as_view(), name='group-messages'),
]
