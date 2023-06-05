# Generated by Django 4.2 on 2023-06-03 03:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playground', '0011_remove_films_cost_id_cinema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like_films',
            name='id_user',
        ),
        migrations.AddField(
            model_name='like_films',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]