from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
	location = models.CharField(max_length=50)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.location + " " + self.name

class Game(models.Model):
	team_1 = models.ForeignKey(Team, related_name='team_1')
	team_2 = models.ForeignKey(Team, related_name='team_2')
	score_1 = models.IntegerField(default=0)
	score_2 = models.IntegerField(default=0)
	date = models.DateField()

	def __str__(self):
		return str(self.score_1) + " - " + str(self.team_1) + " ||vs|| " + str(self.team_2) + " - " + str(self.score_2)


class Person(models.Model):
	username = models.CharField(max_length=20)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	
	def __str__(self):
		return self.first_name + " " + self.last_name

class League(models.Model):
	members = models.ManyToManyField(
		User
	)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Week(models.Model):
	year = models.IntegerField()
	num = models.IntegerField()


class GameBet(models.Model):
	game = models.ForeignKey(Game)
	line_val = models.IntegerField()
	ou_val = models.IntegerField()
	line_bet = models.IntegerField()
	ou_bet = models.IntegerField()


class BetSet(models.Model):
	user = models.ForeignKey(User)
	week = models.ForeignKey(Week)
	bets = models.ManyToManyField(GameBet)
	set_num = models.IntegerField()

