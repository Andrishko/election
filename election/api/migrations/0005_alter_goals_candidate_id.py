# Generated by Django 4.1.1 on 2022-11-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_candidates_goals_goals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goals',
            name='candidate_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='api.candidates'),
        ),
    ]