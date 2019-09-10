from django.core.management.base import BaseCommand, CommandError
from app.models import Week, Game, BetCard, Member, User, Team

class Command(BaseCommand):
	help = 'Add Bets for Alex'

	def handle(self, *args, **options):

		user = User.objects.get(username='Stealrs')
		member = Member.objects.get(user=user)
		week = Week.objects.get(num=1)
		team = Team.objects.get(name='Kansas City Chiefs')
		game = Game.objects.get(week = week, team_1=team)
		betcard = BetCard.objects.get(user=member, game=game)
		betcard.line_bet = -1
		betcard.save()

		team2 = Team.objects.get(name='San Francisco 49ers')
		game2 = Game.objects.get(week = week, team_1=team2)
		betcard2 = BetCard.objects.get(user=member, game=game2)
		betcard2.ou_bet = -1
		betcard2.save()

