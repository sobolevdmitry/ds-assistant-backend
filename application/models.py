from django.db import models
from .utils.gmaps import reverse_geocode

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_last(cls):
        location = cls.objects.last()
        if not location.country and not location.locality:
            data = reverse_geocode(location.latitude, location.longitude)
            try:
                result = data['results'][0]
                for component in result['address_components']:
                    for component_type in component['types']:
                        if component_type == 'country':
                            location.country = component['long_name']
                        elif component_type == 'locality':
                            location.locality = component['long_name']
            except:
                pass
            location.save()
        return location

    @classmethod
    def exclude(cls):
        return ['latitude', 'longitude']

class Sleep(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @classmethod
    def exclude(cls):
        return []

class Steps(models.Model):
    value = models.IntegerField()
    measured_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = "steps"

    @classmethod
    def exclude(cls):
        return []

class Weight(models.Model):
    value = models.IntegerField()
    measured_at = models.DateTimeField()

    @classmethod
    def exclude(cls):
        return []

class Workout(models.Model):
    workout_id = models.CharField(primary_key=True, max_length=64)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    calories = models.IntegerField()

    @classmethod
    def exclude(cls):
        return ['start_date', 'calories']

class Mood(models.Model):
    rate = models.IntegerField()
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()

    @classmethod
    def get_available(cls):
        return dict([
            (0, {'emoji': '💩', 'name': 'shitty'}),
            (1, {'emoji': '😭', 'name': 'unhappy'}),
            (2, {'emoji': '😟', 'name': 'worried'}),
            (3, {'emoji': '🙂', 'name': 'alright'}),
            (4, {'emoji': '🤗', 'name': 'happy'}),
            (5, {'emoji': '🤩', 'name': 'pumped'}),
        ])

    @classmethod
    def exclude(cls):
        return ['description']
