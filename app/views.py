from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.http import Http404
from django.utils.crypto import get_random_string

from .models import Team, Game, League, Membership, Week, Member
from .forms import LeagueForm, JoinLeagueForm, EditBetForm, UserCreateForm
from django.forms import formset_factory
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
		form = UserCreateForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			user = form.save()
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)

			member = Member.objects.create(user=user, betCard=_get_initial_betcard())
			member.save()
			return redirect('/user')
	else:
		form = UserCreateForm()
	return render(request, 'app/signup.html', {'form': form})		

# helper method to render user homepage
@login_required(login_url='/login')
def render_user(request, person_id):
	person = User.objects.get(id=person_id)
	my_leagues = League.objects.filter(members__id = person_id)
	
	active_weeks = Week.objects.filter(status=1)
	locked_weeks = Week.objects.filter(status=2)
	past_weeks = Week.objects.filter(status=3)

	member = Member.objects.get(user=person)

	betting_open = False
	active_week = []
	if len(active_weeks):
		active_week = active_weeks[0]
		betting_open = True
	elif len(locked_weeks):
		active_week = locked_weeks[0]

	past_week_tuples = []
	active_games = []
	results_scores = []
	if len(past_weeks):
		for week in past_weeks:
			games = Game.objects.filter(week=week)
			past_bets = []
			for game in games:
				line_bet, ou_bet = member.get_bet_tuple(game.index)
				score = member.get_game_score(game.index)
				past_bets.append((game, [line_bet, ou_bet, score]))
			week_score = member.get_week_score(week)
			past_week_tuples.append((week, past_bets))
			results_scores.append((week, week_score))
	if active_week:
		games = Game.objects.filter(week=active_week)
		for game in games:
			line_bet, ou_bet = member.get_bet_tuple(game.index)
			score = member.get_game_score(game.index)
			active_games.append((game, [line_bet, ou_bet, score]))
		week_score = member.get_week_score(active_week)
		results_scores.append((active_week, week_score))

	context = {
		'person' : person,
		'my_leagues' : my_leagues,
		'active_games' : active_games, 
		'past_week_tuples' : past_week_tuples, 
		'betting_open' : betting_open, 
		'results_scores' : results_scores
	}
	return render(request, 'app/user.html', context)

# helper method to render league page
@login_required(login_url='/login')
def render_league(request, league_id):
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	if request.user not in my_users:
		raise Http404("User is not a member of requested League.")

	weeks = Week.objects.filter(status__in=[1,2,3])
	members = Member.objects.filter(user__in=my_users)

	results_scores = []
	for week in weeks:
		weekly_scores = []
		for member in members:
			week_score = member.get_week_score(week)
			weekly_scores.append(week_score)
		results_scores.append((week, weekly_scores))

	standings = [0] * len(members)
	for week_tuple in results_scores:
		for i, score in enumerate(week_tuple[1]):
			standings[i] += score

	context = {
		'league' : league,
		'my_users' : my_users,
		'results_scores' : results_scores,
		'standings' : standings
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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
				return redirect('/user')
	else:
		auth_form = AuthenticationForm()
	return render(request, 'app/login.html', {'auth_form':auth_form})

def log_out(request):
	logout(request)
	return redirect('/')

@login_required(login_url='/login')
def edit_picks(request):
	EditBetFormSet = formset_factory(EditBetForm, extra=0)

	# Get games that are currently open (week->status==1)	
	try:
		week = Week.objects.get(status=1)
	except Week.DoesNotExist:
		raise Http404("No games are currently open to betting.")
	games = Game.objects.filter(week=week)
	
	if request.method == 'POST':
		formset = EditBetFormSet(request.POST, request.FILES)
		if formset.is_valid():
			member = Member.objects.get(user=request.user)			
			for form in formset:
				game_id = form.cleaned_data['game_id']
				user = request.user
				game = Game.objects.get(index=game_id)
				line_bet = form.cleaned_data['line_bet']
				ou_bet = form.cleaned_data['ou_bet']
				member.set_betcard(game.index, line_bet, ou_bet)
			member.save()
		return redirect('/user')
	else:
		formset = EditBetFormSet(initial=_generate_form_info(request,games))

	context = {
		'week': week,
        'games': games,
        'edit_bet_formset': formset,
    }
	return render(request, 'app/edit_picks.html', context)

@login_required(login_url='/login')
def league_week(request, league_id, week_num):

	week = Week.objects.get(num=week_num)
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	if request.user not in my_users:
		raise Http404("User is not a member of requested League.")

	games = Game.objects.filter(week=week)
	members = Member.objects.filter(user__in=my_users)

	bet_grid = []
	for game in games:
		game_columns = game.get_column_headers()
		for ind, column in enumerate(game_columns):
			user_bets = []
			for member in members:
				member_val = member.get_column_val(ind, game)
				user_bets.append(member_val)
			bet_grid.append((column, user_bets))

	week_scores = []
	for member in members:
		week_score = member.get_week_score(week)
		week_scores.append(week_score)

	context = {
		'league' : league,
		'bet_grid' : bet_grid,
		'week_scores' : week_scores,
		'my_users' : my_users, 
		'week': week
	}

	return render(request, 'app/league_week.html', context)


def _get_initial_betcard():
	to_ret = chr(32 + 44) * 400
	return to_ret

# Helper method to generate inital bet forms
def _generate_form_info(request, games):
	bet_list = []	
	user = request.user
	member = Member.objects.get(user=user)

	for game in games:
		line_bet, ou_bet = member.get_bet_tuple(game.index)
		dict_entry = dict([("game_id", game.index), ("line_bet", line_bet), ("ou_bet", ou_bet)])
		bet_list.append(dict_entry)

	print ("Generated Betlist: " + str(bet_list))

	return bet_list






