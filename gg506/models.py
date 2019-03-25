from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.gis.db import models
TRANSIT_MODES = (
    (1, 'Transit'),
    (2, 'Driving'),
    (3, 'Private'),
)


class City(models.Model):
    name = models.CharField(max_length=50,blank=True)
    population=models.IntegerField(default=0)
    geom = models.GeometryField(srid=4326)

    def __str__(self):
        return self.name

class Persona(models.Model):
    name = models.CharField(max_length=50, blank=True)
    arrive_by=models.FloatField(default=0.0)
    leave_at=models.FloatField(default=0.0)
    mode = models.CharField(max_length=8, blank=True)
    day= models.CharField(max_length=8, blank=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    city_to=models.ForeignKey(City, on_delete=models.CASCADE,related_name='city_to')
    city_from=models.ForeignKey(City, on_delete=models.CASCADE,related_name='city_from')
    persona=models.ForeignKey(Persona, on_delete=models.CASCADE)
    transit_mode=models.IntegerField(choices=TRANSIT_MODES)
    total_distance=models.FloatField(default=0.0)
    total_time=models.FloatField(default=0.0)
    total_cost=models.FloatField(default=0.0)
    start_time=models.FloatField(default=0.0)
    transfer_time=models.FloatField(default=0.0)
    eager_time=models.FloatField(default=0.0)
    geom = models.GeometryField(srid=4326)

    def __str__(self):
        return self.city_from.name+" to "+self.city_to.name+" mode: "+self.get_transit_mode_display()+" persona "+self.persona.name


class Da(models.Model):
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    total_cost= models.FloatField(default=0.0)
    geom = models.GeometryField(srid=4326)

class Hub(models.Model):
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    transit_mode = models.IntegerField(choices=TRANSIT_MODES)
    is_main = models.BooleanField(default=False)
    geom = models.GeometryField(srid=4326)

    def __str__(self):
        return self.city.name + " Mode: " + self.get_transit_mode_display() + " Name " + self.name+ " Is Main " + str(self.is_main)

class InteraRoute(models.Model):
    da = models.ForeignKey(Da, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    total_distance = models.FloatField(default=0.0)
    total_time = models.FloatField(default=0.0)
    total_cost = models.FloatField(default=0.0)
    geom = models.GeometryField(srid=4326)

    def __str__(self):
        return self.da.city.name + " Da " + str(self.da.id)
