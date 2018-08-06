from django.contrib import admin
from django.contrib.auth.models import User

from .models import Team, Game, League, Bet, Membership, Week

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Week)
admin.site.register(Membership)
admin.site.register(Bet)
