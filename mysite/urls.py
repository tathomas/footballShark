"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import re_path as url
from django.conf.urls import include
from django.contrib import admin 
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^', include('app.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), {'template_name': 'registration/password_reset_done.html'},  name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
