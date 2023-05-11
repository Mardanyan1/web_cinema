from django.db import models
from registration.models import Profile

# Create your models here.
class TEST_Like_films(models.Model):
    name = models.CharField('Название', max_length=50)
    cost = models.FloatField('Цена фильма')
    rent = models.FloatField('Цена аренды фильма')
    
    def __str__(self):
        return self.name
    
class Cinemas(models.Model):
    name = models.CharField(max_length=20, null=True)
    page = models.TextField(null=True)
    id_cinema = models.IntegerField(primary_key=True)
    photo = models.ImageField(null=True)

class Films(models.Model):
    name = models.CharField(max_length=70, null=True)
    link = models.URLField(null=True)
    # description = models.TextField(null=True)
    id_film = models.IntegerField(primary_key=True)
    photo = models.URLField(null=True)

class Films_cost(models.Model):
    purchase = models.DecimalField(max_digits=19, decimal_places=4, null=True)
    rental = models.DecimalField(max_digits=19, decimal_places=4, null=True)
    id_filmRequest = models.IntegerField(primary_key=True)
    id_film = models.ForeignKey(Films, null=True, on_delete=models.SET_NULL)
    id_cinema = models.ForeignKey(Cinemas, null=True, on_delete=models.SET_NULL)

class Like_films(models.Model):
    id_filmRequest = models.ForeignKey(Films_cost, on_delete=models.CASCADE)
    id_user = models.ForeignKey('registration.Profile', on_delete=models.CASCADE)
