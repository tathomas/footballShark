from collections import defaultdict

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.http import Http404

from .models import Team, Game, League, GameBet, BetSet

def home(request):
	all_teams = Team.objects.all()
	context = {
		'all_teams' : all_teams,
	}
	return render(request, 'app/index.html', context)

def faq(request):
	return render(request, 'app/faq.html', {})

# helper method to render user homepage
def render_user(request, person_id):
	person = User.objects.get(id=person_id)
	my_leagues = person.league_set.all()
	
	context = {
		'person' : person,
		'my_leagues' : my_leagues,
	}
	return render(request, 'app/user.html', context)

def user(request, person_id):
	render_user(request, person_id)

def league(request, league_id):
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	context = {
		'league' : league,
		'my_users' : my_users,
	}
	return render(request, 'app/league.html', context)

def league_week(request, betset_id):
	return HttpResponse("You're looking at league week %s." % betset_id)

def user_week(request, betset_id):
	betset = BetSet.objects.get(id=betset_id)
	my_bets = betset.gamebet_set.all()
	context = {
		'betset' : betset,
		'my_bets' : my_bets,
	}
	return render(request, 'app/userweek.html', context)

def vote(request, game_id):
	return HttpResponse("You're voting on game %s." % game_id)

def register(request):
	return HttpResponse("You're looking at the register screen.")


def log_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		render_user(request, user.id)
	else:
		return render(request, 'app/faq.html')	
