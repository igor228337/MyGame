from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    name = models.CharField(max_length=100)
    strength = models.IntegerField()
    agility = models.IntegerField()
    intelligence = models.IntegerField()
    luck = models.IntegerField()

    def __str__(self):
        return self.name

class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card1 = models.ForeignKey(Card, related_name='card1_games', on_delete=models.CASCADE)
    card2 = models.ForeignKey(Card, related_name='card2_games', on_delete=models.CASCADE)
    winner = models.ForeignKey(Card, related_name='winning_games', on_delete=models.CASCADE, null=True, blank=True)
    user_choice = models.ForeignKey(Card, related_name='user_choices', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} vs {self.card1} and {self.card2}"
