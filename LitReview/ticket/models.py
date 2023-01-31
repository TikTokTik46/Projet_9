from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, verbose_name='Description', blank=True)
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Critique(models.Model):
    headline = models.CharField(max_length=128, verbose_name='Titre de la critique')
    body = models.TextField(max_length=8192, verbose_name='Critique')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    time_created = models.DateTimeField(auto_now_add=True),
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)