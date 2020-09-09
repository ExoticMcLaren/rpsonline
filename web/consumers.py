import json
import uuid
import datetime as dt
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Game, Player, PlayerList


class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'lobby_%s' % self.scope["user"].username

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        user = text_data_json['player']

        if action == "ready":
            player_ready = PlayerList.objects.get(player__name__username=user)
            player_ready.ready_to_play = True
            player_ready.save()

            player_list = PlayerList.objects.filter(ready_to_play=True)
            if player_list.count() >= 2:
                p1 = player_list[0].player
                p2 = player_list[1].player
                room = str(uuid.uuid4()).replace('-', '')

                Game.objects.create(creator=p1, opponent=p2, creator_move='N', opponent_move='N', room=room)

                p1_ready = PlayerList.objects.get(player=p1)
                p2_ready = PlayerList.objects.get(player=p2)
                p1_ready.ready_to_play = False
                p2_ready.ready_to_play = False
                p1_ready.save()
                p2_ready.save()

                async_to_sync(self.channel_layer.group_send)(
                    "lobby_%s" % p1,
                    {
                        'type': 'chat_message',
                        'message': room
                    }
                )
                async_to_sync(self.channel_layer.group_send)(
                    "lobby_%s" % p2,
                    {
                        'type': 'chat_message',
                        'message': room
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'chat.message',
                        'message': 'Waiting for opponents...'
                    }
                )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        user = text_data_json['player']
        game = Game.objects.get(room=self.room_name)
        message = ""

        if action == 'move':
            option = text_data_json['option']
            creator = game.creator.name.username
            opponent = game.opponent.name.username

            if user == creator:
                game.creator_move = option
                game.save()
            elif user == opponent:
                game.opponent_move = option
                game.save()

            p1 = Player.objects.get(name=game.creator.name)
            p2 = Player.objects.get(name=game.opponent.name)

            if game.creator_move != "N" and game.opponent_move != "N":
                if game.creator_move == "R" and game.opponent_move == "R":
                    message = "%s choice: %s. %s choice: %s. Tie" % (game.creator, game.creator_move, game.opponent, game.opponent_move)
                    p1.ties += 1
                    p2.ties += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "R" and game.opponent_move == "P":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.opponent)
                    p1.loses += 1
                    p2.wins += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "R" and game.opponent_move == "S":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.creator)
                    p1.wins += 1
                    p2.loses += 1
                    p1.save()
                    p2.save()

                elif game.creator_move == "P" and game.opponent_move == "R":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.creator)
                    p1.wins += 1
                    p2.loses += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "P" and game.opponent_move == "P":
                    message = "%s choice: %s. %s choice: %s. Tie" % (game.creator, game.creator_move, game.opponent, game.opponent_move)
                    p1.ties += 1
                    p2.ties += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "P" and game.opponent_move == "S":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.opponent)
                    p1.loses += 1
                    p2.wins += 1
                    p1.save()
                    p2.save()

                elif game.creator_move == "S" and game.opponent_move == "R":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.opponent)
                    p1.loses += 1
                    p2.wins += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "S" and game.opponent_move == "P":
                    message = "%s choice: %s. %s choice: %s. %s wins!" % (game.creator, game.creator_move, game.opponent, game.opponent_move, game.creator)
                    p1.wins += 1
                    p2.loses += 1
                    p1.save()
                    p2.save()
                elif game.creator_move == "S" and game.opponent_move == "S":
                    message = "%s choice: %s. %s choice: %s. Tie" % (game.creator, game.creator_move, game.opponent, game.opponent_move)
                    p1.ties += 1
                    p2.ties += 1
                    p1.save()
                    p2.save()

                elif game.creator_move == "T":
                    message = "Timeout: %s. %s wins!" % (game.creator, game.opponent)
                    p1.loses += 1
                    p2.wins += 1
                    p1.save()
                    p2.save()
                elif game.opponent_move == "T":
                    message = "Timeout: %s. %s wins!" % (game.opponent, game.creator)
                    p1.wins += 1
                    p2.loses += 1
                    p1.save()
                    p2.save()

                game.completed = dt.datetime.now()
                game.save()

            elif game.creator_move == "T" and game.opponent_move == "T":
                message = "Timeout"
            elif game.creator_move == "N" and game.opponent_move != "N":
                message = "Waiting for %s" % game.creator
            elif game.creator_move != "N" and game.opponent_move == "N":
                message = "Waiting for %s" % game.opponent

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        if action == 'retry':
            game.creator_move = "N"
            game.opponent_move = "N"
            game.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': 'retry'
                }
            )


    def chat_message(self, event):
        message = event['message']

        if message == 'retry':
            self.send(text_data=json.dumps({
                'type': 'retry',
                'message': ''
            }))
        else:
            self.send(text_data=json.dumps({
                'type': 'end',
                'message': message
            }))
