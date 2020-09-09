from django.urls import path
from . import views


urlpatterns = [
    path('api/user/', views.UserListCreate.as_view()),
    path('api/player/', views.PlayerListCreate.as_view()),
    path('api/playerlist/', views.PlayerListListCreate.as_view()),
    path('api/game/', views.GameListCreate.as_view()),
    path('api/statistics/', views.PlayerStatisticsListCreate.as_view()),
]
