from django.core.management.base import BaseCommand, CommandError
from app.models import Week, Game

class Command(BaseCommand):
	help = 'Add Lines for a week - this also unlocks those games for betting'

	def add_arguments(self, parser):
		parser.add_argument('week', nargs='+', type=int)


	def handle(self, *args, **options):

		# Try to find that week
		week_num = 0 + options['week'][0]
		week = Week.objects.get(num=week_num)
		try:
			games = Game.objects.filter(week=week)
		except Week.DoesNotExist or Game.DoesNotExist:
			CommandError('That week could not be found')

		# Set the Previous week as a past week
		past_weeks = Week.objects.filter(num=week_num-1)
		if len(past_weeks):
			past_week = past_weeks[0]
			past_week.SetPast()
			past_week.save()

		# Input lines for each game
		for game in games:
			print('Add Lines for ' + str(game))
			line_input = input("Line? ")
			line_val = int(line_input)
			spread_input = input("Spread? ")
			spread_val = int(spread_input)
			game.line_val = line_val
			game.ou_val = spread_val
			game.save()

		week.Unlock()
		week.save()
