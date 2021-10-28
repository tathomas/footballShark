from django.core.management.base import BaseCommand, CommandError
from app.models import Team, Week, Game
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

		members = Member.objects.all()

		for member in members:
			card = BetCard.objects.create(user=member, game=game)
			card.save()


	def handle(self, *args, **options):

		# Load Teams
		self.add_game()
