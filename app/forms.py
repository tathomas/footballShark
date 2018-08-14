from django import forms
from django.forms.widgets import NumberInput
from django.core.validators import MaxValueValidator, MinValueValidator
from app.models import League, Member

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
	game_id = forms.IntegerField()
	line_bet = forms.IntegerField(min_value=-3, max_value=3,  widget=RangeInput)
	ou_bet = forms.IntegerField(min_value=-3, max_value=3, widget=RangeInput)

	class Meta:
		fields = ('game_id', 'line_bet', 'ou_bet')

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
