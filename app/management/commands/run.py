from django.core.management.base import BaseCommand, CommandError
from app.models import Week, Game

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

				print(game)
				print("\n\n########################################################\n\n")
			else:
				print("Invalid...")

	def add_new_lines(self, week):
		try:
			games = Game.objects.filter(week=week)
		except Week.DoesNotExist or Game.DoesNotExist:
			CommandError('That week could not be found')

		# Set the Previous week as a past week
		past_weeks = Week.objects.filter(num=week.num-1)
		if len(past_weeks):
			past_week = past_weeks[0]
			past_week.SetPast()
			past_week.save()

		# Input lines for each game
		for game in games:
			print('Add Lines for ' + str(game))
			line_input = input("Line? ")
			line_val = float(line_input)
			spread_input = input("Spread? ")
			spread_val = float(spread_input)
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
			week = Week.objects.get(num=1)
			return self.add_new_lines(week)

		if state == 1:
			answer = ""
			while answer != "y" and answer != "n":
				answer = input("Would you like to lock week " + str(active_week.num) + "? (y/n)")
			if answer == "y":
				active_week.Lock()
				active_week.save()
			return 0
		elif state == 2:
			answer = ""
			while answer != "1" and answer != "2" and answer != "3":
				answer = input("Would you like to add scores for week " + str(active_week.num) + ", or add lines for week " + str(active_week.num+1) + ", or quit? (1/2/3)")
			if answer == "1":
				return self.add_scores_prompt(active_week)
			elif answer == "2":
				answer2 = ""
				while answer2 != "y" and answer2 != "n":
					answer2 = input("Are you sure? This will set the previous week as past, and unlock next week. (y/n)")
				if answer2 == "y":
					next_week = Week.objects.get(num=active_week.num+1)
					return self.add_new_lines(next_week)
			return 0

		else:
			CommandError('Invalid state ' + str(state))



