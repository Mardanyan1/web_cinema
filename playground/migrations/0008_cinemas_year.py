# Generated by Django 4.2 on 2023-05-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0007_alter_cinemas_id_cinema_alter_films_id_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinemas',
            name='year',
            field=models.CharField(max_length=20, null=True),
        ),
    ]