from django.core.management.base import CommandError
from django.db import models
from django.contrib.auth.models import User


# Represents one member of the app. Wrapper of django User 
# model in order to reuse Django authentication. 
class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	betCard = models.CharField(max_length=400)

	def __str__(self):
		return super(Member, self).__str__()

	# Sets the bet for this user for a single game.
	def set_betcard(self, game_index, line_bet, ou_bet):
		game = Game.objects.get(index=game_index)
		try:
			card = BetCard.objects.get(game=game, user=self)
		except BetCard.DoesNotExist:
			CommandError('Bet could not be found')

		card.line_bet = line_bet
		card.ou_bet = ou_bet
		card.save()

	# Gets the score for this user for a given week.
	def get_week_score(self, week):
		games = Game.objects.filter(week=week)
		score = 0
		for game in games:
			score += self.get_game_score(game.index)
		return score

	# Gets the score for this user for a given game.
	def get_game_score(self, game_index):
		game = Game.objects.get(index=game_index)
		# game score not updated yet, return 0.
		if not game.score_updated:
			return 0

		try:
			card = BetCard.objects.get(game=game, user=self)
		except BetCard.DoesNotExist:
			CommandError('Bet could not be found')

		return card.score

	# Helper to get the user's bet for a given game.
	def get_bet_tuple(self, game_index):
		game = Game.objects.get(index=game_index)		
		try:
			card = BetCard.objects.get(game=game, user=self)
		except BetCard.DoesNotExist:
			CommandError('Bet could not be found')

		return card.line_bet, card.ou_bet
		
# Static data on a single NFL team
class Team(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def icon_name(self):
		return str.split(self.name, " ")[-1].strip()

# Represents a single week of games.
class Week(models.Model):
	year = models.IntegerField()
	num = models.IntegerField()
	
	# Current status of this week.
	# 0 -> Not started
	# 1 -> Lines added, betting in progress
	# 2 -> Bets locked, games in progress
	# 3 -> Scores locked, week is finished
	# 4 -> Archived from previous year.
	# Note that only a single week at a time has status 1 or 2.
	status = models.IntegerField(default=0)

	# Setters for the week status.
	def Unlock(self):
		self.status = 1

	def Lock(self):
		self.status = 2

	def SetPast(self):
		self.status = 3

	def SetArchived(self):
		self.status = 4

	def __str__(self):
		return "Week " + str(self.num) + ", " + str(self.year) + ". Status: " + str(self.status)

# Represents a single game. Contains the static information on the game, 
# and is updated with line/o_u and then scores as the season progresses.
class Game(models.Model):
	team_1 = models.ForeignKey(Team, related_name='team_1', on_delete=models.CASCADE)
	team_2 = models.ForeignKey(Team, related_name='team_2', on_delete=models.CASCADE)
	score_1 = models.IntegerField(default=0)
	score_2 = models.IntegerField(default=0)
	date = models.DateField()
	index = models.IntegerField(default=0, unique=True)
	week = models.ForeignKey(Week, on_delete=models.CASCADE)
	line_val = models.DecimalField(default=0.0, decimal_places=1, max_digits=3)
	ou_val = models.DecimalField(default=0.0, decimal_places=1, max_digits=3)
	score_updated = models.BooleanField(default=False)


	def __str__(self):
		return str(self.score_1) + " - " + str(self.team_1) + " ||vs|| " + str(self.team_2) + " - " + str(self.score_2)

	@property
	def printSpreadInfo(self):
		return (self.line_val)
	
	def printAwaySpreadInfo(self):
		return ((self.line_val)*(-1))

	def printOvUnInfo(self):
		return  (self.ou_val)

	# Generates column headers for this game. Used by User and League_Week views.
	def get_column_headers(self):

		col_1 = (str(self.team_1.icon_name()), str(self.score_1),  str(self.team_2.icon_name()) , str(self.score_2), " (" + str(self.line_val) + ")")
		col_2 = ("Over", str(self.score_1+self.score_2), "Under", str(self.score_1+self.score_2),  "(" + str(self.ou_val) + ")")
		return [col_1, col_2]
	
	def get_league_headers(self):

		away_team = str(self.team_1.icon_name())
		away_score = (self.score_1)
		home_team = str(self.team_2.icon_name()) 
		home_score = (self.score_2)
		spread_val = (self.line_val)
		total_game_score = (self.score_1+self.score_2)
		ovun_val = (self.ou_val)
		return [away_team,away_score,home_team,home_score,spread_val,ovun_val,total_game_score]

	# Get background colors to use for this game. Returns four colors
	def get_colors(self):

		home_col = away_col = over_col = under_col = "white"

		if self.score_updated:
			if (self.score_1 - self.score_2 < self.line_val):
				home_col="success"
				away_col="danger"
			elif (self.score_1 - self.score_2 > self.line_val):
				away_col="success"
				home_col="danger"
			if (self.score_1 + self.score_2 > self.ou_val):
				over_col ="success"
				under_col="danger"
			elif (self.score_1 + self.score_2 < self.ou_val):
				under_col ="success"
				over_col="danger"
		return away_col, home_col, under_col, over_col

# Represents a set of users who have access to each other's bets.
class League(models.Model):
	members = models.ManyToManyField(User, through='Membership')
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.name

# Relationship between members and leagues
class Membership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	date_joined = models.DateField()
	is_commish = models.BooleanField(default=False)

# Represents a single bet per user, per game. 
class BetCard(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	user = models.ForeignKey(Member, on_delete=models.CASCADE)
	line_bet = models.IntegerField(default=0)
	ou_bet = models.IntegerField(default=0)
	score = models.IntegerField(default=0)

	def calculate_score(self):
		self.score = 0
		if (self.game.score_1 - self.game.score_2 < self.game.line_val):
			self.score += self.line_bet
		elif (self.game.score_1 - self.game.score_2 > self.game.line_val):
			self.score -= self.line_bet
		if (self.game.score_1 + self.game.score_2 > self.game.ou_val):
			self.score += self.ou_bet
		elif (self.game.score_1 + self.game.score_2 < self.game.ou_val):
			self.score -= self.ou_bet

		week_num = self.game.week.num
		multiplier = 1
		if week_num > 20:
			multiplier += week_num - 20

		self.score *= multiplier

		self.save()
		





