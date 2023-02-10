from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from user_follow.models import UserFollow
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from itertools import chain
from django.db.models import CharField, Value

from . import forms, models


# Create your views here.
@login_required
def flux(request):
    users_followed = UserFollow.objects.filter(user=request.user)
    users_in_flux = [obj.followed_user for obj in users_followed] + [request.user]
    tickets_unreviewed = models.Ticket.objects.filter(Q(user__in=users_in_flux) & Q(critique__isnull=True))
    tickets_reviewed = models.Ticket.objects.filter(Q(user__in=users_in_flux) & Q(critique__isnull=False))
    critiques = models.Critique.objects.filter(Q(user__in=users_in_flux) | Q(ticket__in=models.Ticket.objects.filter(user=request.user)))
    tickets_unreviewed = tickets_unreviewed.annotate(content_type=Value('TICKET_UNREVIEWED', CharField()))
    tickets_reviewed = tickets_reviewed.annotate(content_type=Value('TICKET_REVIEWED', CharField()))
    critiques = critiques.annotate(content_type=Value('CRITIQUE', CharField()))
    posts = sorted(
        chain(critiques, tickets_unreviewed, tickets_reviewed),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'ticket/flux.html', context={'posts': posts})

@login_required
def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    critiques = models.Critique.objects.filter(user=request.user)
    critiques = critiques.annotate(content_type=Value('CRITIQUE', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(critiques, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    print(posts)
    return render(request, 'ticket/posts.html', context={'posts': posts})

class TicketDeleteView(DeleteView):
    model = models.Ticket
    success_url = reverse_lazy('posts')
    template_name = 'ticket/ticket_delete_view.html'

class TicketUpdateView(UpdateView):
    model = models.Ticket
    fields = ['title', 'description', 'image']
    success_url = reverse_lazy('posts')
    template_name = 'ticket/ticket_update_view.html'

class CritiqueDeleteView(DeleteView):
    model = models.Critique
    success_url = reverse_lazy('posts')
    template_name = 'ticket/critique_delete_view.html'

class CritiqueUpdateView(UpdateView):
    model = models.Critique
    fields = ['headline', 'rating', 'body']
    success_url = reverse_lazy('posts')
    template_name = 'ticket/critique_update_view.html'

@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
# commit=False permet de ne pas sauvegarder directement le formulaire dans la base de donnée et nous permet de faire des modifications avant le .save()
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    return render(request, 'ticket/ticket_upload.html', context={'form': form})

@login_required
def critique_on_new_ticket_upload(request):
    ticket_form = forms.TicketForm(prefix='ticket')
    critique_form = forms.CritiqueForm(prefix='critique')
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        critique_form = forms.CritiqueForm(request.POST)
        if all([ticket_form.is_valid(), critique_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            critique = critique_form.save(commit=False)
            ticket.user = request.user
            critique.user = request.user
            critique.ticket = ticket
            print(ticket.time_created)
            print(critique.time_created)
            ticket.save()
            critique.save()
            return redirect('flux')
    context = {
    'ticket_form': ticket_form,
    'critique_form': critique_form,
    }
    return render(request, 'ticket/critique_on_new_ticket.html', context=context)

def critique_on_existing_ticket_upload(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    critique_form = forms.CritiqueForm()
    if request.method == 'POST':
        critique_form = forms.CritiqueForm(request.POST)
        if critique_form.is_valid():
            critique = critique_form.save(commit=False)
            critique.user = request.user
            critique.ticket = ticket
            print(critique.time_created)
            critique.save()
            return redirect('flux')
    context = {
        'critique_form': critique_form, 'ticket': ticket
    }
    return render(request, 'ticket/critique_on_existing_ticket.html', context=context)
