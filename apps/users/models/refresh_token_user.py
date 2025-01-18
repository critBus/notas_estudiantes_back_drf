from django.db import models

from .user import User


class RefreshTokenUser(models.Model):
    access_token = models.CharField(max_length=500, db_index=True)
    refresh_token = models.CharField(max_length=500, db_index=True)
    creation_date = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, null=True, blank=True
    )
    vaned = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.access_token}"
