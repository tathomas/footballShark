from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.http import Http404
from django.utils.crypto import get_random_string

from .models import Team, Game, League, GameBet, BetSet, Membership
from .forms import LeagueForm, JoinLeagueForm
import datetime

def home(request):	
	if request.method == 'POST':
		auth_form = AuthenticationForm(request=request, data=request.POST)
		if auth_form.is_valid():
			username = auth_form.cleaned_data.get('username')
			password = auth_form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				render_user(request, user.id)
			else:
				return render(request, 'app/signin.html', {'auth_form':auth_form})
	auth_form = AuthenticationForm()
	context = {
		'auth_form' : auth_form
	}
	return render(request, 'app/index.html', context)

def faq(request):
	return render(request, 'app/faq.html', {})

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			#form.save()
			user = form.save()
			#user = authenticate(username=username, password=raw_password)
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)
			return redirect('/app/user')
	else:
		form = UserCreationForm()
	return render(request, 'app/signup.html', {'form': form})		

# helper method to render user homepage
@login_required(login_url='/app/login')
def render_user(request, person_id):
	person = User.objects.get(id=person_id)
	my_leagues = League.objects.filter(members__id = person_id)
	
	context = {
		'person' : person,
		'my_leagues' : my_leagues,
	}
	return render(request, 'app/user.html', context)

# helper method to render league page
@login_required(login_url='/app/login')
def render_league(request, league_id):
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	if request.user not in my_users:
		raise Http404("User is not a member of requested League.")
	context = {
		'league' : league,
		'my_users' : my_users,
	}
	return render(request, 'app/league.html', context)	

def user(request):
	return render_user(request, request.user.id)

def _get_league_key():
	for i in range(1,1000):
		new_key = get_random_string(10)
		if len(League.objects.filter(key=new_key)) == 0:
			return True, new_key
	return False, ''

@login_required(login_url='/app/login')
def create_league(request):
	if request.method == 'POST':
		form = LeagueForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data.get('name')
			status, new_key = _get_league_key()
			if status:
				league = League.objects.create(name=name, key=new_key)
				league.save()
				current_user = request.user
				membership = Membership(user=current_user, league=league, date_joined=datetime.date.today(), is_commish=True)
				membership.save()
				return render_league(request, league.id)
			else:	
				raise form.ValidationError('Unable to create a unique league key - please try submitting again.')
	else:
		form = LeagueForm()
	return render(request, 'app/create_league.html', {'form':form})

@login_required(login_url='/app/login')
def join_league(request):
	if request.method == 'POST':
		form = JoinLeagueForm(request.POST)
		if form.is_valid():
			league_key = form.cleaned_data.get('key')
			league = League.objects.filter(key=league_key)
			if len(league) != 0:
				current_user = request.user
				if len(Membership.objects.filter(user=current_user.id, league=league[0].id)) != 0:
					form.add_error('key', 'You are already a member of this league!')
				else:
					membership = Membership(user=current_user, league=league[0], date_joined=datetime.date.today(), is_commish=False)
					membership.save()
					return render_league(request, league[0].id)
			else:
				form.add_error('key', 'This is an invalid key. Please try again.')
	else:
		form = JoinLeagueForm()
	return render(request, 'app/join_league.html', {'form':form})

def league(request, league_id):
	return render_league(request, league_id)

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

def log_in(request):
	if request.method == 'POST':
		auth_form = AuthenticationForm(request=request, data=request.POST)
		print(auth_form.errors)
		if auth_form.is_valid():
			username = auth_form.cleaned_data.get('username')
			password = auth_form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/app/user')
	else:
		auth_form = AuthenticationForm()
	return render(request, 'app/login.html', {'auth_form':auth_form})

def log_out(request):
	logout(request)
	return redirect('/app/')
