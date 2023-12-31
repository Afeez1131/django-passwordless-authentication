from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return self.user