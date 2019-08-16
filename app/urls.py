from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

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
	# /app/{password reset and change}
    #url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'},  name='password_reset_done'),
	#url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    #url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
	#url('', include('django.contrib.auth.urls')),
	# /app/user
	url(r'^user$', views.user, name='user'),
	# /app/league/{{league.id}}
	url(r'^league/(?P<league_id>[0-9]+)/$', views.league, name='league'),
	# /app/create_league
	url(r'^create_league$', views.create_league, name='create_league'),
	# /app/join_league
	url(r'^join_league$', views.join_league, name='join_league'),
	# /app/edit_bets/
	url(r'^edit_picks/$', views.edit_picks, name='edit_picks'),
	# /app/league_week/{{league.id}}/{{week}}
	url(r'^league_week/(?P<league_id>[0-9]+)/(?P<week_num>[0-9]+)/$', views.league_week, name='league_week'),

]
