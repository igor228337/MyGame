from django.urls import path
from django.views.generic import TemplateView
from .views import GetRandomCardsView, ChooseWinnerView, GameHistoryView

urlpatterns = [
    path('game/', TemplateView.as_view(template_name='game.html'), name='game'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('get-cards/', GetRandomCardsView.as_view(), name='get_cards'),
    path('choose-winner/', ChooseWinnerView.as_view(), name='choose_winner'),
    path('game-history/', GameHistoryView.as_view(), name='game_history'),
]