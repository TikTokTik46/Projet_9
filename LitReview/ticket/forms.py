from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class CritiqueForm(forms.ModelForm):
    RATING_CHOICES = [(i, i) for i in range(0, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES,
                               widget=forms.RadioSelect)

    class Meta:
        model = models.Critique
        fields = ['headline', 'rating', 'body']
