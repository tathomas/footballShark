from django import forms
from django.forms.widgets import NumberInput
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models import League, Member, Game

from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RangeInput(NumberInput):
    input_type = 'range'

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

	class Meta:
		fields = ('game_id', 'line_bet', 'ou_bet')

	def __init__(self, *args, **kwargs):
		inital_list = kwargs.pop('initial')
		super().__init__(*args, **kwargs)

		game_id = inital_list['game_id']
		line_bet = inital_list['line_bet']
		ou_bet = inital_list['ou_bet']


		line_id = "x-" + str(game_id) + "-line_bet"
		ou_id = "x-" + str(game_id) + "-ou_bet"

		self.fields['game_id'] = forms.IntegerField(initial=game_id)
		self.fields['line_bet'] = forms.IntegerField(initial=line_bet, min_value=-3, max_value=3,  widget=RangeInput(attrs={'id':line_id, 'class':"bet_field", 'oninput': 'update(this.id);'}))
		self.fields['ou_bet'] = forms.IntegerField(initial=ou_bet, min_value=-3, max_value=3, widget=RangeInput(attrs={'id':ou_id, 'class':"bet_field", 'oninput': 'update(this.id);'}))


	def get_game(self):
		game_id=self.fields['game_id']
		return Game.objects.get(index=game_id)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
