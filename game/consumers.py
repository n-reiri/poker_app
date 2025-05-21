import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Player, Action

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'room_{self.room_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data    = json.loads(text_data)
        action  = data.get('action')
        amount  = data.get('amount', 0)
        user    = self.scope['user']
        result  = await self.update_player_and_record(user, self.room_id, action, amount)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_message',
                'message': result,
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def update_player_and_record(self, user, room_id, action, amount):
        player = Player.objects.get(user=user, room__id=room_id)

        # チップ更新ロジック
        if action in ('bet', 'raise'):
            player.chips -= int(amount)

        player.save()

        # アクション履歴を作成
        Action.objects.create(
            player=player,
            action=action,
            amount=amount if action in ('bet', 'raise', 'call') else None
        )

        return {
            'player_id': player.id,
            'action':    action,
            'amount':    amount,
            'chips':     player.chips,
        }