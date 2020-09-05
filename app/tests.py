from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Game, League, Membership, Week, Member, BetCard

from . import views

from datetime import datetime

class ModelUnitTests(TestCase):

	# Setup database test data for unit testing
	@classmethod
	def setUpTestData(cls):
		cls.team1 = Team.objects.create(name="Bills")
		cls.team2 = Team.objects.create(name="Dolphins")
		cls.team3 = Team.objects.create(name="Jets")

		cls.week1 =  Week.objects.create(year=2020,num=1)
		cls.week2 =  Week.objects.create(year=2020,num=2)

		date_string = "September 520198:20 PM"
		date_time = datetime.strptime(date_string, '%B %d%Y%I:%M %p')
		cls.game1 = Game.objects.create(team_1=cls.team1,
										team_2=cls.team2,
										date=date_time,
										week=cls.week1, index=1)
		cls.game2 = Game.objects.create(team_1=cls.team1,
										team_2=cls.team3,
										date=date_time,
										week=cls.week2, index=2)	

		cls.user1 = User.objects.create_user(username='member1',
										email='normal@user.com',
										password='foo')

		cls.member1 = Member.objects.create(user=cls.user1)
		views._create_initial_betcards(cls.member1)

	# Test for Member model
	def test_member(self):
		# Before anything, all scores should be zero
		self.assertEqual(self.member1.get_week_score(self.week1), 0)
		self.assertEqual(self.member1.get_week_score(self.week2), 0)
		self.assertEqual(self.member1.get_game_score(1), 0)
		self.assertEqual(self.member1.get_game_score(2), 0)

		print (self.member1)
		#lion = Member.objects.get(user=)
		#cat = Animal.objects.get(name="cat")
		#self.assertEqual(lion.speak(), 'The lion says "roar"')
		#self.assertEqual()


	# Test for Game model
	def test_game(self):
		# Before anything, should print empty spread info
		self.assertEqual(self.game1.printSpreadInfo, "Spread: 0.0  Over/Under: 0.0")

		self.assertEqual(1,2)
		












