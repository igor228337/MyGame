from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Card, GameHistory


class GameAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.card1 = Card.objects.create(name="Card 1", strength=5, agility=5, intelligence=5, luck=5)
        self.card2 = Card.objects.create(name="Card 2", strength=6, agility=6, intelligence=6, luck=6)

    def test_get_random_cards(self):
        url = reverse('get_cards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    def test_choose_winner(self):
        url = reverse('choose_winner')
        data = {
            "card1": self.card1.id,
            "card2": self.card2.id,
            "user_choice": self.card1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['winner'], self.card2.id)

    def test_game_history(self):
        GameHistory.objects.create(
            user=self.user,
            card1=self.card1,
            card2=self.card2,
            winner=self.card2,
            user_choice=self.card1,
        )

        url = reverse('game_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['winner']['id'], self.card2.id)
