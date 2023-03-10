from django.conf import settings
from django.db import models


class UserFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      verbose_name="Utilisateur à suivre :",
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
