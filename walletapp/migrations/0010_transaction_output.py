# Generated by Django 3.2.2 on 2021-05-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0009_alter_transaction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='output',
            field=models.CharField(default='pending', max_length=1000),
        ),
    ]
