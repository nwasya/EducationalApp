from django.urls import path

from Edu_game.views import get_category, start_play, get_results
from Edu_register.views import register_page

urlpatterns = [
    path('category', get_category, name='category'),
    path('play/<game_id>', start_play, name='play'),
    path('results/<game_id>', get_results, name='results'),
]
