from django import forms
from app.models import League
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class LeagueForm(forms.ModelForm):
	name = forms.CharField(max_length=100)

	class Meta:
		model = League
		fields = ('name',)

class JoinLeagueForm(forms.Form):
	key = forms.CharField(max_length=20)

	class Meta:
		model = League
		fields = ('key')



