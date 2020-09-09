from django.contrib.auth.models import User
from rest_framework import generics

from .models import Player, PlayerList, Game
from .serializers import UserSerializer, PlayerSerializer, PlayerListSerializer, GameSerializer

# Create your views here.


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlayerListCreate(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerStatisticsListCreate(generics.ListCreateAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        user = self.request.user
        return Player.objects.filter(name=user)

class PlayerListListCreate(generics.ListCreateAPIView):
    queryset = PlayerList.objects.all()
    serializer_class = PlayerListSerializer


class GameListCreate(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
