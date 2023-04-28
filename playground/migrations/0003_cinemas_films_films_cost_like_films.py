# Generated by Django 4.2 on 2023-04-17 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('playground', '0002_rename_like_films_test_like_films'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinemas',
            fields=[
                ('name', models.CharField(max_length=20, null=True)),
                ('page', models.TextField(null=True)),
                ('id_cinema', models.IntegerField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Films',
            fields=[
                ('name', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('id_film', models.IntegerField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Films_cost',
            fields=[
                ('purchase', models.DecimalField(decimal_places=4, max_digits=19, null=True)),
                ('rental', models.DecimalField(decimal_places=4, max_digits=19, null=True)),
                ('id_filmRequest', models.IntegerField(primary_key=True, serialize=False)),
                ('id_cinema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playground.cinemas')),
                ('id_film', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playground.films')),
            ],
        ),
        migrations.CreateModel(
            name='Like_films',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_filmRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.films_cost')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.profile')),
            ],
        ),
    ]
