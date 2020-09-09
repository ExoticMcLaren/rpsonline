from django.contrib import admin
from .models import Player, PlayerList, Game

# Register your models here.

admin.site.register(Player)
admin.site.register(PlayerList)
admin.site.register(Game)
