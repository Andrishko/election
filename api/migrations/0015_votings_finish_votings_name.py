# Generated by Django 4.1.1 on 2022-11-17 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_votings_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='votings',
            name='finish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='votings',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]