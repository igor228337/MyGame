from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Card, GameHistory, Race
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
                races = Race.objects.all()
                if not races:
                    raise ValueError("Нет доступных рас. Создайте расы в базе данных.")

                race = random.choice(races)
                base_strength = random.randint(1, 10)
                base_agility = random.randint(1, 10)
                base_intelligence = random.randint(1, 10)
                base_luck = random.randint(1, 10)
                base_health = 100 + base_strength

                strength = base_strength * race.strength_multiplier
                agility = base_agility * race.agility_multiplier
                intelligence = base_intelligence * race.intelligence_multiplier
                luck = base_luck * race.luck_multiplier
                health = base_health * race.health_multiplier
                fake = Faker().name()

                existing_card = Card.objects.filter(
                    strength=strength,
                    agility=agility,
                    intelligence=intelligence,
                    luck=luck,
                    health=health,
                    race=race
                ).first()

                if not existing_card:
                    card = Card.objects.create(
                        name=fake,
                        strength=strength,
                        agility=agility,
                        intelligence=intelligence,
                        luck=luck,
                        health=health,
                        race=race
                    )
                    new_cards.append(card)
                    break
                else:
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
            (card.strength) +
            (card.agility) +
            (card.intelligence) +
            (card.luck)
        )


class GameHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        history = GameHistory.objects.filter(user=user).order_by('-created_at')
        serializer = GameHistorySerializer(history, many=True)
        return Response(serializer.data)
