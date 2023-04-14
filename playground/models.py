from django.db import models

# Create your models here.
class Like_films(models.Model):
    name = models.CharField('Название', max_length=50)
    cost = models.FloatField('Цена фильма')
    rent = models.FloatField('Цена аренды фильма')
    
    def __str__(self):
        return self.name