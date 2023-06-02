from django.db import models

# Create your models here.
class TEST_Like_films(models.Model):
    name = models.CharField('Название', max_length=50)
    cost = models.FloatField('Цена фильма')
    rent = models.FloatField('Цена аренды фильма')
    
    def __str__(self):
        return self.name
    
class Cinemas(models.Model):
    id_cinema = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    page = models.TextField(null=True)
    photo = models.ImageField(null=True)

class Films(models.Model):
    id_film = models.AutoField(primary_key=True)
    film_name = models.CharField(max_length=70, null=True)
    year = models.CharField(max_length=20, null=True)
    # description = models.TextField(null=True)
    photo = models.URLField(null=True)

    def __str__(self):
        return self.film_name
    

class Films_Cost(models.Model):
    viewing_method = models.CharField(max_length=20, null=True)
    quality = models.CharField(max_length=15, null=True)
    cost = models.DecimalField(max_digits=19, decimal_places=4, null=True)
    id_filmRequest = models.IntegerField(primary_key=True)
    id_film = models.ForeignKey(Films, null=True, on_delete=models.SET_NULL)
    # id_cinema = models.ForeignKey(Cinemas, null=True, on_delete=models.SET_NULL)


class Like_films(models.Model):
    id_filmRequest = models.ForeignKey(Films_Cost, on_delete=models.CASCADE)
    id_user = models.ForeignKey('registration.Profile', on_delete=models.CASCADE)
