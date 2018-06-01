from django.contrib import admin

from .models import Team, Game, Person, League, GameBet, BetSet

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Person)
admin.site.register(League)
admin.site.register(BetSet)
admin.site.register(GameBet)
