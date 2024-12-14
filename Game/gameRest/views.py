from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Card, GameHistory
from .serializers import CardSerializer, GameHistorySerializer
import random
import logging
from faker import Faker

logger = logging.getLogger(__name__)

class GetRandomCardsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        all_cards = self.generate_new_cards()
        card1, card2 = random.sample(all_cards, 2)

        serializer = CardSerializer([card1, card2], many=True)
        return Response(serializer.data)

    def generate_new_cards(self, count=2):
        new_cards = []
        for _ in range(count):
            while True:
                strength = random.randint(1, 10)
                agility = random.randint(1, 10)
                intelligence = random.randint(1, 10)
                luck = random.randint(1, 10)
                health = 100 + (strength * 1.1)
                fake = Faker().name()
                
                if not Card.objects.filter(strength=strength, agility=agility, intelligence=intelligence, luck=luck, health=health).exists():
                    card = Card.objects.create(
                        name=fake,
                        strength=strength,
                        agility=agility,
                        intelligence=intelligence,
                        luck=luck,
                        health=health
                    )
                    new_cards.append(card)
                    break
                else:
                    existing_card = Card.objects.filter(strength=strength, agility=agility, intelligence=intelligence, luck=luck, health=health).first()
                    new_cards.append(existing_card)
                    break
        return new_cards


class ChooseWinnerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        card1_id = request.data.get('card1')
        card2_id = request.data.get('card2')
        user_choice_id = request.data.get('user_choice')

        try:
            card1 = Card.objects.get(id=card1_id)
            card2 = Card.objects.get(id=card2_id)
            user_choice = Card.objects.get(id=user_choice_id)
        except Card.DoesNotExist:
            return Response({"error": "Карты не найдены"}, status=status.HTTP_404_NOT_FOUND)

        winner = self.determine_winner(card1, card2)

        history = GameHistory.objects.create(
            user=user,
            card1=card1,
            card2=card2,
            winner=winner,
            user_choice=user_choice,
        )

        serializer = GameHistorySerializer(history)
        return Response(serializer.data)

    def determine_winner(self, card1, card2):
        card1_power = self.calculate_total_power(card1)
        card2_power = self.calculate_total_power(card2)

        if card1_power > card2_power:
            return card1
        elif card2_power > card1_power:
            return card2
        else:
            return random.choice([card1, card2])

    def calculate_total_power(self, card):
        return (
            (card.strength * 1.7) +
            (card.agility * 1.6) +
            (card.intelligence * 1.4) +
            (card.luck * 1.1) +
            (card.health)
        )


class GameHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        history = GameHistory.objects.filter(user=user).order_by('-created_at')
        serializer = GameHistorySerializer(history, many=True)
        return Response(serializer.data)