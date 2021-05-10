# Generated by Django 3.2.2 on 2021-05-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0002_auto_20210508_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=128)),
                ('time', models.TimeField()),
                ('hash', models.CharField(max_length=300)),
            ],
        ),
    ]
