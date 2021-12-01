from django.contrib import admin

# Register your models here.
from Edu_game.models import GameCategory, GameScore


class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__']


class ScoreAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'score', 'category']


admin.site.register(GameCategory, GameCategoryAdmin)
admin.site.register(GameScore, ScoreAdmin)
