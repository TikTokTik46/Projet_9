from django import template
import pytz
import locale

# Configure la locale en fr_FR
locale.setlocale(locale.LC_TIME, 'fr_FR')

register = template.Library()


@register.filter
def format_date(value):
    # Définit le fuseau horaire sur Europe/Paris
    paris_tz = pytz.timezone('Europe/Paris')

    # Convertit la valeur de la date en utilisant le fuseau horaire défini
    value = value.astimezone(paris_tz)

    # Formate la date et l'heure en utilisant la locale
    # et le fuseau horaire définis
    return value.strftime("%H:%M, %d %B %Y")
