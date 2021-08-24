from django.core.management.base import BaseCommand, CommandError
from app.models import Team, Week, Game, Member, BetCard
import pandas as pd
from datetime import datetime

class Command(BaseCommand):
	help = 'Load in all team objects'

	def load_games(self):
            team1 = Team.objects.get(name = 'Indianapolis Colts')
            team2 = Team.objects.get(name = 'Buffalo Bills')
        
            week, created = Week.objects.get_or_create(year=2020, num = 18)

            if created:
                print ("Week: " + str(week))
            print ("Created: " + str (created))

            game = Game.objects.create(team_1=team1,
                                        team_2=team2,
                                        date=pd.to_datetime("today"),
                                        week=week, index=567)

            game.save()

            team3 = Team.objects.get(name = 'Los Angeles Rams')
            team4 = Team.objects.get(name = 'Seattle Seahawks')
            
            week2, created2 = Week.objects.get_or_create(year=2020, num = 18)

            if created2:
                print ("Week: " + str(week2))
            print ("Created: " + str (created2))

            game2 = Game.objects.create(team_1=team3,
                                        team_2=team4,
                                        date=pd.to_datetime("today"),
                                        week=week2, index=568)

            game2.save()

            members = Member.objects.all()

            for member in members:
                card = BetCard.objects.create(user=member, game=game)
                card.save()

                card2 = BetCard.objects.create(user=member, game=game2)
                card2.save()




	def handle(self, *args, **options):

		# Load Games
		self.load_games()

