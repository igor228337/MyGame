from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import GetRandomCardsViewSet, ChooseWinnerViewSet, GameHistoryViewSet


router = DefaultRouter()
router.register(r'get-cards', GetRandomCardsViewSet, basename='get_cards')
router.register(r'choose-winner', ChooseWinnerViewSet, basename='choose_winner')
router.register(r'game-history', GameHistoryViewSet, basename='game_history')

urlpatterns = [
    path('game/', TemplateView.as_view(template_name='game.html'), name='game'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('api/', include(router.urls)),
]