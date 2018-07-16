from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
	# /app/
	url(r'^$', views.home, name='home'),
	# /app/faq
	url(r'^faq$', views.faq, name='faq'),
	# /app/signup
	url(r'^signup$', views.signup, name='signup'),
	# /app/login
	url(r'^login$', views.log_in, name='log_in'),
	# /app/logout
	url(r'^logout$', views.log_out, name='log_out'),
	# /app/user
	url(r'^user$', views.user, name='user'),
	# /app/league/{{league.id}}
	url(r'^league/(?P<league_id>[0-9]+)/$', views.league, name='league'),
	# /app/create_league
	url(r'^create_league$', views.create_league, name='create_league'),
	# /app/join_league
	url(r'^join_league$', views.join_league, name='join_league'),
	# /app/league/week/{{week.id}}
	url(r'^league/week/(?P<betset_id>[0-9]+)/$', views.league_week, name='league_week'),
	# /app/user/week/{{week.id}}
	url(r'^user/week/(?P<betset_id>[0-9]+)/$', views.user_week, name='user_week'),

	# /app/5/vote/
	url(r'^(?P<game_id>[0-9]+)/vote/$', views.vote, name='vote'),

]
