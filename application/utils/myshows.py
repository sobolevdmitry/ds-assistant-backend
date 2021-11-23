from assistant.settings import MYSHOWS_LOGIN, MYSHOWS_TOKEN
import requests

# todo: refresh token

def get_last_episode():
    try:
        response = requests.post('https://myshows.me/v3/rpc/', headers={
            'Authorization2': f'Bearer {MYSHOWS_TOKEN}',
            'Platform': 'web',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
        }, json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'profile.Feed',
            'params': {
                'login': MYSHOWS_LOGIN
            }
        })
        for feed_item in response.json()['result']:
            if feed_item['type'] == 'e.check':
                return dict(show=feed_item['show'], episode=feed_item['episodes'][-1])
    except:
        pass
    return None
