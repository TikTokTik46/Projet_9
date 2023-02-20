from django.contrib import admin

# Register your models here.
from .models import Ticket, Critique

admin.site.register(Ticket)
admin.site.register(Critique)
