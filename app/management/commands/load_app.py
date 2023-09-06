from django.core.management.base import BaseCommand, CommandError
from app.models import Team, Week, Game
import pandas as pd
import numpy as numpy
from datetime import datetime

class Command(BaseCommand):
	help = 'Load in all team objects'

	def load_teams(self):
		input_data = team_list = ['Buffalo Bills', 'New York Jets', 'New England Patriots', 'Miami Dolphins', 'Pittsburgh Steelers', 'Baltimore Ravens', 'Cleveland Browns', 'Cincinnati Bengals', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Tennessee Titans', 'Denver Broncos', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Philadelphia Eagles', 'Dallas Cowboys', 'Washington Football Team', 'New York Giants', 'Tampa Bay Buccaneers', 'Carolina Panthers', 'Atlanta Falcons', 'New Orleans Saints', 'Green Bay Packers', 'Minnesota Vikings', 'Chicago Bears', 'Detroit Lions', 'San Francisco 49ers', 'Seattle Seahawks', 'Arizona Cardinals', 'Los Angeles Rams']

		for team_name in input_data:
			new_team, created = Team.objects.get_or_create(name=team_name)
			new_team.save()

		#print(Team.objects.all())


	def load_games(self):
		input_data = pd.read_csv("./app/management/Data/2023Games.csv", header=0).loc[:, :'Line']
		my_data = input_data.drop(["Line"],axis=1)

		for (ind, line), in numpy.ndenumerate(my_data.values()):
			team1 = Team.objects.get(name = line[6])
			team2 = Team.objects.get(name = line[5])
			
			week, created = Week.objects.get_or_create(year=2021, num = line[1])

			date_string = (str(line[3]) + str(line[0]) + str(line[4]))
			date_time = datetime.strptime(date_string, '%B %d%Y%I:%M %p')

			if created:
				print ("Week: " + str(week))
			print ("Created: " + str (created) + "Creating game " + str(ind) + ", line: " + str(line))

			game = Game.objects.create(team_1=team1,
										team_2=team2,
										date=date_time,
										week=week, index=ind)

			game.save()


	def handle(self, *args, **options):

		# Load Teams
		self.load_teams()

		# Load Games
		self.load_games()



