from rest_framework import serializers
from .models import Card, GameHistory

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'strength', 'agility', 'intelligence', 'luck', 'health']

class GameHistorySerializer(serializers.ModelSerializer):
    card1 = CardSerializer()
    card2 = CardSerializer()
    winner = CardSerializer()
    user_choice = CardSerializer()

    class Meta:
        model = GameHistory
        fields = ['id', 'card1', 'card2', 'winner', 'user_choice', 'created_at']