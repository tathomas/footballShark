from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	betCard = models.CharField(max_length=400)

	def __str__(self):
		return super(Member, self).__str__()

	def set_betcard(self, game_index, line_bet, ou_bet):
		game = Game.objects.get(index=game_index)
		try:
			card = BetCard.objects.get(game=game, user=self)
		except BetCard.DoesNotExist:
			CommandError('Bet could not be found')

		card.line_bet = line_bet
		card.ou_bet = ou_bet
		card.save()

	def get_week_score(self, week):
		games = Game.objects.filter(week=week)
		score = 0
		for game in games:
			score += self.get_game_score(game.index)
		return score

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

	def get_bet_tuple(self, game_index):
		game = Game.objects.get(index=game_index)		
		try:
			card = BetCard.objects.get(game=game, user=self)
		except BetCard.DoesNotExist:
			CommandError('Bet could not be found')

		return card.line_bet, card.ou_bet
		

class Team(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def icon_name(self):
		return str.split(self.name, " ")[-1].strip()

class Week(models.Model):
	year = models.IntegerField()
	num = models.IntegerField()
	status = models.IntegerField(default=0)

	def Unlock(self):
		self.status = 1

	def Lock(self):
		self.status = 2

	def SetPast(self):
		self.status = 3

	def __str__(self):
		return "Week " + str(self.num) + ", " + str(self.year) + ". Status: " + str(self.status)

class Game(models.Model):
	team_1 = models.ForeignKey(Team, related_name='team_1')
	team_2 = models.ForeignKey(Team, related_name='team_2')
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
		return "Spread: " + str(self.line_val) + "  Over/Under: " + str(self.ou_val)

	def get_column_headers(self):

		col_1 = (str(self.team_1.icon_name()), str(self.score_1),  str(self.team_2.icon_name()) , str(self.score_2), " (" + str(self.line_val) + ")")
		col_2 = ("Over", str(self.score_1+self.score_2), "Under", str(self.score_1+self.score_2),  "(" + str(self.ou_val) + ")")
		return [col_1, col_2]

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


class League(models.Model):
	members = models.ManyToManyField(User, through='Membership')
	name = models.CharField(max_length=100)
	key = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.name

class Membership(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	date_joined = models.DateField()
	is_commish = models.BooleanField(default=False)

	def __str__(self):
		return str(user) + " joined " + str(league) + " on " + str(date_joined)

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
		if week_num > 17:
			multiplier += week_num - 17

		self.score *= multiplier

		self.save()
		





