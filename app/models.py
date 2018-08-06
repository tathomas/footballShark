from django.db import models
from django.contrib.auth.models import User

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
	week = models.ForeignKey(Week, on_delete=models.CASCADE)
	line_val = models.IntegerField(default=0)
	ou_val = models.IntegerField(default=0)


	def __str__(self):
		return str(self.score_1) + " - " + str(self.team_1) + " ||vs|| " + str(self.team_2) + " - " + str(self.score_2)

	@property
	def printSpreadInfo(self):
		return str(self.team_1) + " @ " + str(self.team_2) + ", line=" + str(self.line_val) + "  ou=" + str(self.ou_val)

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



class Bet(models.Model):
	game = models.ForeignKey(Game)
	betslip = models.ForeignKey(User)
	line_bet = models.IntegerField(default=0)
	ou_bet = models.IntegerField(default=0)
	score = models.IntegerField(default=0)

	def updateScore(self, away, home, line, ou):
		self.score = 0
		if(away-home < line):
			self.score += self.line_bet
		elif(away-home > line):
			self.score -= self.line_bet
		if(away+home < ou):
			self.score -= self.ou_bet
		elif(away+home > ou):
			self.score += self.ou_bet

class ScoreCard(models.Model):
	week = models.ForeignKey(Week, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)

	def updateScore(self):
		games = Game.objects.filter(week=self.week)
		for game in games:
			bet = Bet.objects.get(betslip=self.user, game=game)
			self.score += bet.score


