from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    avatarUrl = models.CharField(
        max_length=200,
        default='https://sf1-ttcdn-tos.pstatp.com/img/user-avatar/f4998fe95ef30363f12a04f670579825~300x300.image'
    )
    acceptedCnt = models.IntegerField(default=0)


