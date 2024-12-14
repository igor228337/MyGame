from django.contrib import admin
from .models import Card, GameHistory, Race


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'strength', 'agility', 'intelligence', 'luck')
    list_filter = ('strength', 'agility', 'intelligence', 'luck')
    search_fields = ('name',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'card1', 'card2', 'winner', 'user_choice', 'created_at')
    list_filter = ('user', 'winner', 'created_at')
    search_fields = ('user__username', 'card1__name', 'card2__name')
    readonly_fields = ('created_at',)