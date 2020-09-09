from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(default=0)
    loses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name.username


class PlayerList(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    ready_to_play = models.BooleanField(default=False)

    def __str__(self):
        return self.player.name.username


class Game(models.Model):
    CHOICE = (('R', "Rock"), ('P', "Paper"), ('S', "Scissors"), ('N', "Nothing"), ('T', "Timeout"))

    creator = models.ForeignKey(Player, related_name='creator', on_delete=models.CASCADE)
    opponent = models.ForeignKey(Player, related_name='opponent', null=True, blank=True, on_delete=models.CASCADE)
    creator_move = models.CharField(max_length=15, blank=True, choices=CHOICE)
    opponent_move = models.CharField(max_length=15, blank=True, choices=CHOICE)
    room = models.CharField(max_length=255)

    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
