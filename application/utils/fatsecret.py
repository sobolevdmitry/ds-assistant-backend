from assistant.settings import \
    FATSECRET_ID, FATSECRET_DEVICE_ID, FATSECRET_SECRET_KEY, FATSECRET_USERAGENT, \
    FUEL_CALORIES_TARGET, FUEL_PROTEIN_TARGET, FUEL_FAT_TARGET, FUEL_CARBS_TARGET, \
    PYTZ_TIMEZONE
from datetime import datetime
import uuid
import requests
import xmltodict

def get_food_diary():
    current = dict(calories=0, protein=0, fat=0, carbs=0)
    food_entries = []
    try:
        r = requests.post("https://android.fatsecret.com/android/RecipeJournalDayAndroidPage.aspx", headers={
            'User-Agent': FATSECRET_USERAGENT
        }, data={
            'c_id': FATSECRET_ID,
            'c_s': FATSECRET_SECRET_KEY,
            'c_d': FATSECRET_DEVICE_ID,
            'guid': str(uuid.uuid4()),
            'dt': (datetime.now(tz=PYTZ_TIMEZONE) - datetime(1970, 1, 1, tzinfo=PYTZ_TIMEZONE)).days,
            'c_fl': 1,
            'app_version': '9.5.0.3',
            'fl': 6,
            'lang': 'en',
            'mkt': 'RU',
            'device': 6
        })

        if r.ok:
            data = xmltodict.parse(r.text)['recipejournalday']
            current = dict(calories=data['energyPerDay'], protein=data['proteinPerDay'], fat=data['fatPerDay'], carbs=data['carbohydratePerDay'])
            food_entries = data['recipejournalentry']
            if 'id' in food_entries:
                food_entries = [food_entries]
    except Exception as e:
        print(e)

    return dict(
        target=dict(calories=FUEL_CALORIES_TARGET, protein=FUEL_PROTEIN_TARGET, fat=FUEL_FAT_TARGET, carbs=FUEL_CARBS_TARGET),
        current=current,
        food_entries=food_entries
    )
