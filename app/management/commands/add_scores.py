from django.core.management.base import BaseCommand, CommandError
from app.models import Week, Game, Bet, ScoreCard

class Command(BaseCommand):
	help = 'Add Scores for Games'

	def add_arguments(self, parser):
		parser.add_argument('week', nargs='+', type=int)


	def handle(self, *args, **options):

		week_num = options['week'][0]
		try:
			week=Week.objects.get(num=week_num)
			games = Game.objects.filter(week=week)
		except Week.DoesNotExist or Game.DoesNotExist:
			CommandError('That week could not be found')

		for game in games:
			update_game = input('Add Scores for ' + str(game) + "? (y/n)")
			if update_game != 'y':
				continue
			away_input = input("Away Score? ")
			away_val = int(away_input)
			home_input = input("Home Score? ")
			home_val = int(home_input)
			game.score_1 = away_val
			game.score_2 = home_val
			game.save()

			print(game)

			bets = Bet.objects.filter(game=game)
			for bet in bets:
				bet.updateScore(away_val, home_val, game.line_val, game.ou_val)
				bet.save()

			cards = ScoreCard.objects.filter(week=week)
			for card in cards:
				card.updateScore()
				card.save()


