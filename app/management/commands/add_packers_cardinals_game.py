from django.core.management.base import BaseCommand, CommandError
from app.models import Team, Week, Game, User, Member, BetCard
import pandas as pd
from datetime import datetime

class Command(BaseCommand):


	def add_game(self):


		team1 = Team.objects.get(name = "Green Bay Packers")
		team2 = Team.objects.get(name = "Arizona Cardinals")
		
		week, created = Week.objects.get_or_create(year=2021, num = 8)

		game = Game.objects.create(team_1=team1,
									team_2=team2,
									date=pd.to_datetime("today"),
									week=week, index=284)

		game.save()

		users = User.objects.all()

		for user in users:
			try:
				member = Member.objects.get(user=user)
				card = BetCard.objects.create(user=member, game=game)
				card.save()
			except Member.DoesNotExist:
				member = None


	def handle(self, *args, **options):

		# Load Teams
		self.add_game()
