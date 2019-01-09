from urllib.request import Request,urlopen
import json
import base64

keys = json.loads(open('../data/keys.json','r').read())
API_KEY = keys['mysportsfeeds']
API_PASS = keys['msf_password']
URL = 'https://api.mysportsfeeds.com/v1.0/pull/{}/{}/{}.json' # sports type (nba,nfl,nhl,mlb) ; season type ; endpoint

def get_full_schedule(league):
    if league == 'nfl':
        type = '2019-playoff'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'full_game_schedule'

    q = Request(URL.format(league,type,endpoint))
    q.add_header('Authorization', 'Basic ' + base64.b64encode('{}:{}'.format(API_KEY,API_PASS).encode('utf-8')).decode('ascii'))

    games = json.loads(urlopen(q).read())

    return games['fullgameschedule']['gameentry']

#print(get_full_schedule('nba')[0])
