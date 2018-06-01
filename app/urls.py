from django.conf.urls import url

from . import views

app_name = 'app'
urlpatterns = [
	# /app/
	url(r'^$', views.index, name='index'),
	# /app/5/
	url(r'^(?P<team_id>[0-9]+)/$', views.detail, name='detail'),

	# /app/user/{{person.id}}
	url(r'^user/(?P<person_id>[0-9]+)/$', views.user, name='user'),
	# /app/league/{{league.id}}
	url(r'^league/(?P<league_id>[0-9]+)/$', views.league, name='league'),
	# /app/league/week/{{week.id}}
	url(r'^league/week/(?P<betset_id>[0-9]+)/$', views.league_week, name='league_week'),
	# /app/user/week/{{week.id}}
	url(r'^user/week/(?P<betset_id>[0-9]+)/$', views.user_week, name='user_week'),

	# /app/5/vote/
	url(r'^(?P<game_id>[0-9]+)/vote/$', views.vote, name='vote'),

	url(r'^register/$', views.register, name='register'),
]
