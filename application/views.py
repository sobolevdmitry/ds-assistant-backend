from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.forms.models import model_to_dict
from assistant.settings import APP_API_KEY
from .models import Location, Sleep, Steps, Weight, Workout, Mood
from .utils.myshows import get_last_episode
from .utils.spotify import get_current_song
from .utils.fatsecret import get_food_diary
import json

@csrf_exempt
def write(request):
    if request.headers.get('x-api-key') != APP_API_KEY:
        return JsonResponse({'ok': False, 'error': 'Wrong API key'})
    try:
        body = json.loads(request.body)
        data = body['data']
        if body['entity'] == 'location':
            # iOS location format: {"coords": {"accuracy": 5, "altitude": 0, "altitudeAccuracy": -1, "heading": -1, "latitude": 55.5807481, "longitude": 36.8251304, "speed": -1}, "timestamp": 1630923717786.8108}
            last = Location.objects.all().last()
            if last is None or (last.latitude != float(data['coords']['latitude']) and last.longitude != float(data['coords']['longitude'])):
                location = Location(latitude=float(data['coords']['latitude']), longitude=float(data['coords']['longitude']))
                location.save()
                return JsonResponse({'ok': True, 'id': location.id})
            else:
                return JsonResponse({'ok': False, 'error': 'Already exists'})
        elif body['entity'] == 'sleep':
            # iOS sleep format: {"sourceId": "com.apple.Health", "sourceName": "Health", "startDate": "2021-09-06T13:01:00.000+0300", "endDate": "2021-09-06T14:01:00.000+0300", "value": "INBED"}
            last = Sleep.objects.filter(end_date__gt=data['startDate']).last()
            if last is None:
                sleep = Sleep(start_date=data['startDate'], end_date=data['endDate'])
                sleep.save()
                return JsonResponse({'ok': True, 'id': sleep.id})
            else:
                return JsonResponse({'ok': False, 'error': 'Already exists'})
        elif body['entity'] == 'steps':
            # iOS steps format: {"endDate": "2021-09-06T14:11:00.000+0300", "startDate": "2021-09-06T14:11:00.000+0300", "value": 100}
            last = Steps.objects.all().last()
            if last is None or last.value != data['value']:
                steps = Steps(value=data['value'], measured_at=data['endDate'])
                steps.save()
                return JsonResponse({'ok': True, 'id': steps.id})
            else:
                return JsonResponse({'ok': False, 'error': 'Already exists'})
        elif body['entity'] == 'weight':
            # iOS weight format: {"endDate": "2021-09-04T19:23:00.000+0300", "startDate": "2021-09-04T19:23:00.000+0300", "value": 34926.61249}
            last = Weight.objects.all().last()
            if last is None or last.value != int(data['value']):
                weight = Weight(value=int(data['value']), measured_at=data['endDate'])
                weight.save()
                return JsonResponse({'ok': True, 'id': weight.id})
            else:
                return JsonResponse({'ok': False, 'error': 'Already exists'})
        elif body['entity'] == 'workouts':
            ids = []
            for item in data:
                # iOS workout format: {"activityId": 3000, "activityName": "Other", "calories": 0, "device": "iPhone13,2", "distance": 0, "end": "2021-09-03T19:58:00.000+0300", "id": "8FAAC28D-CC65-4ECB-8418-1AF2CA5A754A", "metadata": {"HKWasUserEntered": 1}, "sourceId": "com.apple.Health", "sourceName": "Health", "start": "2021-09-03T19:33:00.000+0300", "tracked": false}
                existing_workout = Workout.objects.filter(pk=item['id'])
                if not existing_workout:
                    workout = Workout(pk=item['id'], start_date=item['start'], end_date=item['end'],
                                      calories=item['calories'])
                    workout.save()
                    ids.append(workout.pk)
            if len(ids) > 0:
                return JsonResponse({'ok': True, 'ids': ids})
            else:
                return JsonResponse({'ok': False, 'error': 'Already exists'})
        return JsonResponse({'ok': False, 'error': 'No available entity provided'})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

@csrf_exempt
def read(request):
    if request.headers.get('x-api-key') != APP_API_KEY:
        return JsonResponse({'ok': False, 'error': 'Wrong API key'})
    try:
        body = json.loads(request.body)
        entity = None
        if body['entity'] == 'location':
            entity = Location.get_last()
        elif body['entity'] == 'sleep':
            entity = Sleep.objects.last()
        elif body['entity'] == 'steps':
            entity = Steps.objects.last()
        elif body['entity'] == 'weight':
            entity = Weight.objects.last()
        elif body['entity'] == 'workout':
            entity = Workout.objects.order_by('-end_date').first()
        elif body['entity'] == 'mood':
            entity = Mood.objects.last()
        if entity:
            return JsonResponse({'ok': True, 'entity': model_to_dict(entity, exclude=entity.exclude())})
        else:
            return JsonResponse({'ok': False, 'error': 'No ' + body['entity'] + ' data yet'})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': e})

@csrf_exempt
def get_data(request):
    data = dict()
    data['mood'] = model_to_dict(Mood.objects.last(), exclude=Mood.exclude())
    if data['mood']['rate'] < 3:
        data['mood']['rate'] = 3
    data['mood'] = {**data['mood'], **Mood.get_available()[data['mood']['rate']]}
    data['location'] = model_to_dict(Location.get_last(), exclude=Location.exclude())
    data['sleep'] = model_to_dict(Sleep.objects.last(), exclude=Sleep.exclude())
    data['steps'] = model_to_dict(Steps.objects.last(), exclude=Steps.exclude())
    data['weight'] = model_to_dict(Weight.objects.last(), exclude=Weight.exclude())
    data['workout'] = model_to_dict(Workout.objects.order_by('-end_date').first(), exclude=Workout.exclude())
    data['series'] = cache.get('data-series')
    if data['series'] is None:
        data['series'] = get_last_episode()
        cache.set('data-series', data['series'], 5 * 60)
    data['song'] = cache.get('data-song')
    if data['song'] is None:
        data['song'] = get_current_song()
        cache.set('data-song', data['song'], 1 * 60)
    data['fuel'] = cache.get('data-fuel')
    if data['fuel'] is None:
        data['fuel'] = get_food_diary()
        cache.set('data-fuel', data['fuel'], 5 * 60)
    return JsonResponse(data)
