from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from authentication.models import User


@login_required
def user_followed(request):
    user_follow_request = models.UserFollow.objects.filter(user=request.user)
    users_followed = User.objects.exclude(
        pk__in=[user.followed_user.pk for user in user_follow_request] +
               [request.user.pk])
    users_following = models.UserFollow.objects. \
        filter(followed_user=request.user)
    user_follow_form = forms.UserFollowForm(followed=users_followed)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            user_follow_form = forms.UserFollowForm(request.POST,
                                                    followed=users_followed)
            if user_follow_form.is_valid():
                user_follow = user_follow_form.save(commit=False)
                user_follow.user = request.user
                user_follow.save()
                return redirect('users_followed')
        if action == 'delete':
            object_id = request.POST.get('object_id')
            obj = models.UserFollow.objects.get(pk=object_id)
            obj.delete()
            return redirect('users_followed')
    context = {
        'user_follow_form': user_follow_form,
        'user_follow_request': user_follow_request,
        'users_following': users_following,
    }
    return render(request, 'user_follow/user_followed.html', context=context)
