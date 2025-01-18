from django.db import models

from .user import User


class BlackListedTokenAccess(models.Model):
    token = models.CharField(max_length=500, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    timestamp = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.token
