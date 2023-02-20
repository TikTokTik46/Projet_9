"""LitReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView, LogoutView,\
    PasswordChangeView, PasswordChangeDoneView
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import ticket.views
import user_follow.views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('flux/', ticket.views.flux, name='flux'),
    path('posts/', ticket.views.posts, name='posts'),
    path('ticket/upload/', ticket.views.ticket_upload, name='ticket_upload'),
    path('critique/upload', ticket.views.critique_on_new_ticket_upload,
         name='critique_on_new_ticket_upload'),
    path('critique/<int:ticket_id>/upload',
         ticket.views.critique_on_existing_ticket_upload,
         name='critique_on_existing_ticket_upload'),
    path('delete_ticket/<int:pk>/', ticket.views.TicketDeleteView.as_view(),
         name='delete_ticket'),
    path('delete_critique/<int:pk>/', ticket.views.
         CritiqueDeleteView.as_view(), name='delete_critique'),
    path('update_ticket/<int:pk>/', ticket.views.TicketUpdateView.as_view(),
         name='update_ticket'),
    path('update_critique/<int:pk>/', ticket.views.
         CritiqueUpdateView.as_view(), name='update_critique'),
    path('users-followed', user_follow.views.user_followed,
         name='users_followed'),
]
# Permet de rendre les photos accéssible par le biais d'une URL
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
