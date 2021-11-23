from django.contrib import admin
from .models import Location, Sleep, Steps, Weight, Workout, Mood

@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = ['created_at', 'latitude', 'longitude', 'country', 'locality']

@admin.register(Sleep)
class Sleep(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']

@admin.register(Steps)
class Steps(admin.ModelAdmin):
    list_display = ['measured_at', 'value']

@admin.register(Weight)
class Weight(admin.ModelAdmin):
    list_display = ['measured_at', 'value']

@admin.register(Workout)
class Workout(admin.ModelAdmin):
    list_display = ['workout_id', 'start_date', 'end_date', 'calories']

@admin.register(Mood)
class Mood(admin.ModelAdmin):
    list_display = ['created_at', 'rate', 'description']
