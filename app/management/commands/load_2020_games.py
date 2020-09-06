from django.core.management.base import BaseCommand, CommandError
from app.models import Team, Week, Game, Member, BetCard
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
	help = 'Load in all team objects'

	def archive_2019_games(self):
		
		# Games in 2019 were mistakenly labelled as 2018.
		weeks = Week.objects.filter(year=2018)
		for week in weeks:
			week.SetArchived()
			week.save()

	def load_2020_games(self):
		input_data = pd.read_csv("./app/management/Data/2020Games.csv", header=0).loc[:, :'Line']
		my_data = input_data.drop(["Line"],axis=1)

		members = Member.objects.all()

		for ind, line in enumerate(my_data.as_matrix()):
			team1 = Team.objects.get(name = line[6])
			team2 = Team.objects.get(name = line[5])
			
			week, created = Week.objects.get_or_create(year=2020, num = line[1])

			date_string = (str(line[3]) + str(line[0]) + str(line[4]))
			date_time = datetime.strptime(date_string, '%B %d%Y%I:%M %p')

			# 2020 games start at index=300 instead of 0.
			index = 300 + ind

			if created:
				print ("Week: " + str(week))
			print ("Created: " + str (created) + "Creating game " + str(index) + ", line: " + str(line))

			game = Game.objects.create(team_1=team1,
										team_2=team2,
										date=date_time,
										week=week, index=index)

			game.save()

			for member in members:
				card = BetCard.objects.create(user=member, game=game)
				card.save()

	def remove_2020_games(self):
		
		weeks = Week.objects.filter(year=2020).delete()


	def handle(self, *args, **options):

		# Archive 2019 weeks
		self.archive_2019_games()

		# Load Games
		self.load_2020_games()

		#self.remove_2020_games()