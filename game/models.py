from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    """ゲーム部屋"""
    name        = models.CharField(max_length=50, unique=True)
    host        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_rooms')
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    """部屋に参加したプレイヤー情報（所持チップなど）"""
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players')
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_players')
    chips     = models.PositiveIntegerField(default=1000)
    is_dealer = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"

class Action(models.Model):
    """ベット・チェック・フォールドなどのアクション履歴"""
    player    = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='actions')
    timestamp = models.DateTimeField(auto_now_add=True)
    action    = models.CharField(
                  max_length=20,
                  choices=[
                    ('bet',   'Bet'),
                    ('fold',  'Fold'),
                    ('call',  'Call'),
                    ('check', 'Check'),
                    ('raise', 'Raise'),
                  ]
               )
    amount    = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.user.username} – {self.action} ({self.amount})"