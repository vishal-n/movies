# Generated by Django 4.0.3 on 2022-10-13 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='admin', max_length=20),
        ),
    ]
