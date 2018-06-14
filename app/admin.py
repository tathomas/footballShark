from django.contrib import admin
from django.contrib.auth.models import User

from .models import Team, Game, League, GameBet, BetSet, Week

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Week)
admin.site.register(BetSet)
admin.site.register(GameBet)
