# ✨ `ds-assistant-backend`

Django application for collecting data from different sources and providing it via API.
- Frontend available @ [ds-assistant-frontend](https://github.com/sobolevdmitry/ds-assistant-frontend)
- iOS app available @ [ds-assistant-ios](https://github.com/sobolevdmitry/ds-assistant-ios)

## 🔧 Setup

- Clone this repository and create a new folder `var`
- Install requirements from `requirements.txt`
- Copy `.env.example` to `.env` and configure your environment variables
- Create database and migrate
- Configure your web server 

## 📊 Third-party services
### iOS app
I use my [iOS app](https://github.com/sobolevdmitry/ds-assistant-ios) to track Apple Health measurements like sleep, weight, workout, steps, and more. It also keeps track of my current location.

### Google Maps Geocoding API
You need [reverse geocoding](https://developers.google.com/maps/documentation/geocoding/overview#ReverseGeocoding) for translating latitude and longitude values into a human-readable address.
Assign `GMAPS_GEOCODE_API_KEY` to your [API key](https://developers.google.com/maps/documentation/geocoding/get-api-key)... or [not yours](https://github.com/search?q=maps.googleapis.com%2Fmaps%2Fapi%2Fgeocode%2Fjson%3Flatlng&type=code).

### FatSecret
I use [FatSecret](https://www.fatsecret.com) to track my nutrition. 
If you want to collect data from FS, you need to set `FATSECRET_*` variables. 
You can get these values simply by inspecting the requests that the application sends. 
I prefer to intercept traffic from their [Android application](https://play.google.com/store/apps/details?id=com.fatsecret.android&hl=en&gl=US).
Also, you need to set your targets `FUEL_*_TARGET`. 

### MyShows
I keep track series I watch with [MyShows](https://myshows.me). If you want to collect this data, you need to set `MYSHOWS_*` variables. They can be easily found in cookies.

### Spotify
I use Spotify Web API to get the tracks I listen to. Just set `SPOTIFY_*` variables using [this tutorial]((https://developer.spotify.com/documentation/web-api/quick-start/)).

### Telegram Bot
I track my daily mood using Telegram Bot. Set `MOODBOT_TOKEN` to your [bot token](https://core.telegram.org/bots/api#authorizing-your-bot) and `MOODBOT_ADMIN_ID` to your Telegram ID.
Start your bot using `start_polling.py`.

## ❤️ Credits

I created this project inspired by [Felix Krause](https://github.com/KrauseFx) and his projects [FxLifeSheet](https://github.com/KrauseFx/FxLifeSheet), [whereisfelix.today](https://github.com/KrauseFx/whereisfelix.today).
