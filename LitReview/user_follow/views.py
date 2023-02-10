from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models

@login_required
def user_followed(request):
    users_followed = models.UserFollow.objects.filter(user=request.user)
    users_following = models.UserFollow.objects.filter(followed_user=request.user)
    user_follow_form = forms.UserFollowForm(followed=users_followed)
    if request.method == 'POST':
        action = request.POST.get('action')
        if 'followed_user' in request.POST:
            user_follow_form = forms.UserFollowForm(request.POST, followed=users_followed)
            if user_follow_form.is_valid():
                user_follow = user_follow_form.save(commit=False)
                user_follow.user = request.user
                user_follow.save()
                redirect('users_followed')
        if action == 'delete':
            object_id = request.POST.get('object_id')
            obj = users_followed.get(pk=object_id)
            obj.delete()
            redirect('users_followed')
    context = {
        'user_follow_form': user_follow_form,
        'user_unfollow_form': users_following,
        'users_followed': users_followed,
        'users_following': users_following,
    }
    return render(request, 'user_follow/user_followed.html', context=context)
