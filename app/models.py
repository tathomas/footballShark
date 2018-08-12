from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	betCard = models.CharField(max_length=400)

	def __str__(self):
		return super(Member, self).__str__()

	def set_betcard(self, game_index, line_bet, ou_bet):
		char_bet = 0
		char_bet += (line_bet + 4) * 10
		char_bet += ou_bet + 4

		temp = self.betCard[:game_index] + chr(char_bet + 32) + self.betCard[game_index+1:]
		self.betCard = temp

	def get_week_score(self, week):
		games = Game.objects.filter(week=week)
		score = 0
		for game in games:
			score += self.get_game_score(game.index)
		return score

	def get_game_score(self, game_index):
		line_bet, ou_bet = self.get_bet_tuple(game_index)

		game = Game.objects.get(index=game_index)
		if not game.score_updated:
			return 0

		score = 0
		if (game.score_1 - game.score_2 < game.line_val):
			print('1')
			score += line_bet
		elif (game.score_1 - game.score_2 > game.line_val):
			print('2')
			score -= line_bet
		if (game.score_1 + game.score_2 > game.ou_val):
			print('3')
			score += ou_bet
		elif (game.score_1 + game.score_2 < game.ou_val):
			print('4')
			score -= ou_bet
		return score

	def get_bet_tuple(self, game_index):
		game = Game.objects.get(index=game_index)
		
		score_char = self.betCard[game_index]

		score_int = ord(score_char) - 32
		line_bet = (score_int // 10) - 4
		ou_bet = (score_int % 10) - 4

		return line_bet, ou_bet

	def get_column_val(self, ind, game):
		line_bet, ou_bet = self.get_bet_tuple(game.index)
		if ind == 0:
			if line_bet < 0:
				return -1 * line_bet
		elif ind == 1:
			if line_bet > 0:
				return line_bet
		elif ind == 2:
			if ou_bet > 0:
				return ou_bet
		elif ind == 3:
			if ou_bet < 0:
				return ou_bet * -1
		return None

class Team(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

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

class Game(models.Model):
	team_1 = models.ForeignKey(Team, related_name='team_1')
	team_2 = models.ForeignKey(Team, related_name='team_2')
	score_1 = models.IntegerField(default=0)
	score_2 = models.IntegerField(default=0)
	date = models.DateField()
	index = models.IntegerField(default=0, unique=True)
	week = models.ForeignKey(Week, on_delete=models.CASCADE)
	line_val = models.IntegerField(default=0)
	ou_val = models.IntegerField(default=0)
	score_updated = models.BooleanField(default=False)


	def __str__(self):
		return str(self.score_1) + " - " + str(self.team_1) + " ||vs|| " + str(self.team_2) + " - " + str(self.score_2)

	@property
	def printSpreadInfo(self):
		return str(self.team_1) + " @ " + str(self.team_2) + ", line=" + str(self.line_val) + "  ou=" + str(self.ou_val)

	def get_column_headers(self):
		col_1 = str(self.team_1) + " (" + str(-1*self.line_val) + ")"
		col_2 = str(self.team_2) + " (" + str(self.line_val) + ")"
		col_3 = "Over (" + str(self.ou_val) + ")"
		col_4 = "Under (" + str(self.ou_val) + ")"
		return col_1, col_2, col_3, col_4

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





