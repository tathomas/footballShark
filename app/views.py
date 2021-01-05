from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.http import Http404
from django.utils.crypto import get_random_string

from .models import Team, Game, League, Membership, Week, Member, BetCard
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

@login_required(login_url='/login')
def user_faq(request):
	return render(request, 'app/user_faq.html', {})

def signup(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			user = form.save()
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, user)

			member = Member.objects.create(user=user)
			member.save()
			_create_initial_betcards(member)
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
	past_weeks = Week.objects.filter(status=3).order_by('num')

	total_score = 0

	member = Member.objects.get(user=person)

	betting_open = False
	active_week = []
	if len(active_weeks):
		active_week = active_weeks[0]
		betting_open = True
	elif len(locked_weeks):
		active_week = locked_weeks[0]

	past_week_data = []
	active_week_tuples = []
	results_scores = []
	if len(past_weeks):
		for week in past_weeks:
			games = Game.objects.filter(week=week)
			past_week_tuples = []
			for game in games:
				user_bets = [(),()]
				columns = game.get_column_headers()
				cols = game.get_colors()
				line_bet, ou_bet = member.get_bet_tuple(game.index)
				if line_bet < 0:
					user_bets[0] = (-1*line_bet, game.team_1.icon_name(), cols[0])
				elif line_bet > 0:
					user_bets[0] = (line_bet, game.team_2.icon_name(), cols[1])
				else:
					user_bets[0] = (0,'', "white")
				if ou_bet < 0:
					user_bets[1] = (-1*ou_bet, "Under", cols[2])
				elif ou_bet > 0:
					user_bets[1] = (ou_bet, "Over", cols[3])
				else:
					user_bets[1] = (0,'', "white")
				my_score = member.get_game_score(game.index)
				if my_score > 0:
					my_col = 'success'
				elif my_score < 0:
					my_col = 'danger'
				else:
					my_col = 'white'
				past_week_tuples.append((columns, user_bets, member.get_game_score(game.index)))
			past_week_data.append((week, past_week_tuples))
			week_score = member.get_week_score(week)
			total_score += week_score
			results_scores.append((week, week_score))
	if active_week:
		games = Game.objects.filter(week=active_week).order_by('index')
		for game in games:
			user_bets = [(),()]
			columns = game.get_column_headers()
			cols = game.get_colors()
			line_bet, ou_bet = member.get_bet_tuple(game.index)
			if line_bet < 0:
				user_bets[0] = (-1*line_bet, game.team_1.icon_name(), cols[0])
			elif line_bet > 0:
				user_bets[0] = (line_bet, game.team_2.icon_name(), cols[1])
			else:
				user_bets[0] = (0,'', "white")
			if ou_bet < 0:
				user_bets[1] = (-1*ou_bet, "Under", cols[2])
			elif ou_bet > 0:
				user_bets[1] = (ou_bet, "Over", cols[3])
			else:
				user_bets[1] = (0,'', "white")
			my_score = member.get_game_score(game.index)
			if my_score > 0:
				my_col = 'success'
			elif my_score < 0:
				my_col = 'danger'
			else:
				my_col = 'white'
			active_week_tuples.append((columns, user_bets, (my_score, my_col)))
		week_score = member.get_week_score(active_week)
		total_score += week_score
		results_scores.append((active_week, week_score))

	context = {
		'person' : person,
		'my_leagues' : my_leagues,
		'active_week_tuples' : active_week_tuples, 
		'past_week_data' : past_week_data, 
		'betting_open' : betting_open, 
		'results_scores' : results_scores,
        'active_week': active_week,
		'total_score': total_score
	}
	return render(request, 'app/user.html', context)

# helper method to render league page
@login_required(login_url='/login')
def render_league(request, league_id):
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	if request.user not in my_users:
		raise Http404("User is not a member of requested League.")

	weeks = Week.objects.filter(status__in=[1,2,3]).order_by('num')
	members = Member.objects.filter(user__in=my_users)

	inverted_weeks = []
	for week in weeks:
		inverted_weeks.insert(0, week)

	results_scores = []
	for player in members:
		weekly_scores = []
		total = 0
		for week in weeks:
			week_score = player.get_week_score(week)
			total += week_score
			weekly_scores.insert(0, week_score)
		results_scores.append((player, total, weekly_scores))

	context = {
		'league' : league,
		'inverted_weeks' : inverted_weeks,
		'results_scores' : results_scores,
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
		formset = EditBetFormSet(request.POST, request.FILES, initial=_generate_form_info(request,games))
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

	week = Week.objects.get(num=week_num, year=2020)
	league = League.objects.get(id=league_id)
	my_users = league.members.all()
	if request.user not in my_users:
		raise Http404("User is not a member of requested League.")

	games = Game.objects.filter(week=week)
	members = Member.objects.filter(user__in=my_users)

	game_columns = []
	for game in games:
		columns = game.get_column_headers()
		for column in columns:
			game_columns.append(column)

	bet_grid = []
	for member in members:
		week_score = member.get_week_score(week)
		if week_score > 0:
			week_score_tup = (week_score, "success")
		elif week_score < 0:
			week_score_tup = (week_score, "danger")
		else:
			week_score_tup = (week_score, "white")
			
		user_bets = []
		for game in games:
			cols = game.get_colors()
			line_bet, ou_bet = member.get_bet_tuple(game.index)
			if line_bet < 0:
				user_bets.append((-1*line_bet, game.team_1.icon_name(), cols[0]))
			elif line_bet > 0:
				user_bets.append((line_bet, game.team_2.icon_name(), cols[1]))
			else:
				user_bets.append((0,'', "white"))
			if ou_bet < 0:
				user_bets.append((-1*ou_bet, "Under", cols[2]))
			elif ou_bet > 0:
				user_bets.append((ou_bet, "Over", cols[3]))
			else:
				user_bets.append((0,'', "white"))

		bet_grid.append((member, week_score_tup, user_bets))

	context = {
		'league' : league,
		'bet_grid' : bet_grid,
		'game_columns' : game_columns,
		'week': week
	}

	return render(request, 'app/league_week.html', context)


def _create_initial_betcards(member):
	games = Game.objects.all()

	for game in games:
		card = BetCard.objects.create(user=member, game=game)
		card.save()

# Helper method to generate inital bet forms
def _generate_form_info(request, games):
	bet_list = []
	user = request.user
	member = Member.objects.get(user=user)

	for game in games:
		line_bet, ou_bet = member.get_bet_tuple(game.index)
		dict_entry = dict([("game_id", game.index), ("line_bet", line_bet), ("ou_bet", ou_bet)])
		bet_list.append(dict_entry)

	return bet_list






