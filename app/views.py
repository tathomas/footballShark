from collections import defaultdict

from django.shortcuts import render
from django.http import HttpResponse

from .models import Team, Game, Person, League, GameBet, BetSet

def index(request):
	all_teams = Team.objects.all()
	context = {
		'all_teams' : all_teams,
	}
#	template = loader.get_template('app/index.html')
#	return HttpResponse(template.render(context, request))
	return render(request, 'app/index.html', context)

def detail(request, team_id):
	return HttpResponse("You're looking at team %s." % team_id)

def user(request, person_id):
	person = Person.objects.get(id=person_id)
	my_leagues = person.league_set.all()
	
	context = {
		'person' : person,
		'my_leagues' : my_leagues,
	}
	return render(request, 'app/user.html', context)

def league(request, league_id):
	league = League.objects.get(id=league_id)
	my_betsets = league.betset_set.all()
	betset_dict = defaultdict(list)
	for betset in my_betsets:
		betset_dict[betset.set_num].append(betset)

	context = {
		'league' : league,
		'betset_dict' : betset_dict,
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



