from django.contrib import admin


from .models import Team, Game, League, Member, Membership, Week, BetCard

admin.site.register(Member)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Week)
admin.site.register(Membership)
admin.site.register(BetCard)

