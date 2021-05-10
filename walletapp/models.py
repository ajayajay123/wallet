from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128)
    private_key = models.TextField(max_length=128)
    public_key = models.TextField(max_length=128)
    user_type = models.IntegerField(default=3)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    uid = models.CharField(max_length=128, primary_key=True)
    time = models.CharField(max_length=200)
    hash = models.CharField(max_length=300)
    output = models.TextField(default="pending")

    class MetaData:
        order = ['time']


class Contract(models.Model):
    contract_id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=500)
    status = models.IntegerField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
