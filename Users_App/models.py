from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True)
    database = models.CharField(max_length=20)

    def __str__(self):
        return self.user_auth.username

    class Meta:
        db_table = 'user_info'
        verbose_name_plural = "Informacion de los usuarios"