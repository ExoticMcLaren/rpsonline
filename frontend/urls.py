from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_index, name='show_index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('game/<str:room_name>/', views.show_game, name='show_game'),
]