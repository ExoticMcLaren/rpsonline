from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Player, PlayerList, Game


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'wins', 'loses', 'ties')


class PlayerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerList
        fields = ('player', 'ready_to_play')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'creator', 'opponent', 'creator_move', 'opponent_move', 'room', 'completed', 'created', 'modified')
