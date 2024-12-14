from rest_framework import serializers
from .models import Card, GameHistory, Race


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'name', 'description']

class CardSerializer(serializers.ModelSerializer):
    race = RaceSerializer()
    class Meta:
        model = Card
        fields = ['id', 'name', 'strength', 'agility', 'intelligence', 'luck', 'health', 'race']

class GameHistorySerializer(serializers.ModelSerializer):
    card1 = CardSerializer()
    card2 = CardSerializer()
    winner = CardSerializer()
    user_choice = CardSerializer()

    class Meta:
        model = GameHistory
        fields = ['id', 'card1', 'card2', 'winner', 'user_choice', 'created_at']