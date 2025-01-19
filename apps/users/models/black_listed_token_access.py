from django.db import models

from apps.users.models.user import User


class BlackListedTokenAccess(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(
        User,
        related_name="user_BlackListedTokenAccess",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
