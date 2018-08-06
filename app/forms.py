from django import forms
from django.forms.widgets import NumberInput
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models import League
from django.contrib.auth.models import User


from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    input_type = 'range'

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

class EditBetForm(forms.Form):
	game_id = forms.IntegerField()
	line_bet = forms.IntegerField(min_value=-3, max_value=3,  widget=RangeInput)
	ou_bet = forms.IntegerField(min_value=-3, max_value=3, widget=RangeInput)

	class Meta:
		fields = ('bet_id', 'line_bet', 'ou_bet')


