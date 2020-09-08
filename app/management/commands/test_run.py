from django.core.management.base import BaseCommand, CommandError
from app.models import Week, Game, BetCard, User, Member
from django.template.loader import render_to_string
from django.core.mail import send_mail


class Command(BaseCommand):
	help = 'Run the app. This contains commands to change the app\'s state'

	def add_scores_prompt(self, week):
		try:
			games = Game.objects.filter(week=week)
		except Week.DoesNotExist or Game.DoesNotExist:
			CommandError('That week could not be found')

		while True:
			answer = ""
			for ind, game in enumerate(games):
				print(str(ind) + " - " + str(game))
			answer = int(input("Choose a game, or (-1) to exit: "))

			if answer == -1:
				return 0
			elif answer > -1 and answer < len(games):
				game = games[answer]
				away_input = input("Away Score? ")
				away_val = int(away_input)
				home_input = input("Home Score? ")
				home_val = int(home_input)
				game.score_1 = away_val
				game.score_2 = home_val
				game.score_updated = True
				game.save()

				cards = BetCard.objects.filter(game=game)
				for card in cards:
					card.calculate_score()

				print(game)
				print("\n\n########################################################\n\n")
			else:
				print("Invalid...")

	def add_fake_new_lines(self, week):
		try:
			games = Game.objects.filter(week=week)
		except Week.DoesNotExist or Game.DoesNotExist:
			CommandError('That week could not be found')

		# Set the Previous week as a past week
		past_weeks = Week.objects.filter(num=week.num-1, year=2020)
		if len(past_weeks):
			past_week = past_weeks[0]
			past_week.SetPast()
			past_week.save()

		# Input lines for each game
		for game in games:
			line_val = 1
			spread_val = 1
			game.line_val = line_val
			game.ou_val = spread_val
			game.save()

		week.Unlock()
		week.save()

		return 0

	def handle(self, *args, **options):

		print("########################################################")
		print("### Run ...")
		print("########################################################\n")
		print("### Current state:\n")

		active_weeks = Week.objects.filter(status=1)
		locked_weeks = Week.objects.filter(status=2)
		past_weeks = Week.objects.filter(status=3)

		state = 0
		if len(active_weeks) > 0:
			state = 1
			active_week = active_weeks[0]
			print("Active week: " + str(active_week.num))
		elif len(locked_weeks) > 0:
			state = 2
			active_week = locked_weeks[0]
			print("Active week: " + str(active_week.num))

		if state == 0:
			print("This is a newly loaded app - please add lines for Week 1")
			week = Week.objects.get(num=1, year=2020)
			self.add_fake_new_lines(week)
			self.send_new_season_email(week)

		if state == 1:

			active_week.Lock()
			active_week.save()

		elif state == 2:

			next_week = Week.objects.get(num=active_week.num+1, year=2020)
			self.add_fake_new_lines(next_week)

		else:
			CommandError('Invalid state ' + str(state))
