from django import forms

from . import models


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollow
        fields = ['followed_user']

    def __init__(self, *args, **kwargs):
        followed = kwargs.pop('followed')
        super().__init__(*args, **kwargs)
        self.fields['followed_user'].queryset = followed
