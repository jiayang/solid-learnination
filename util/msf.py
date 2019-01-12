from urllib.request import Request,urlopen
import json
import base64

keys = json.loads(open('data/keys.json','r').read())
API_KEY = keys['mysportsfeeds']
API_PASS = keys['msf_password']
URL = 'https://api.mysportsfeeds.com/v1.0/pull/{}/{}/{}.json' # sports type (nba,nfl,nhl,mlb) ; season type ; endpoint

def msf_request(url):
    q = Request(url)
    q.add_header('Authorization', 'Basic ' + base64.b64encode('{}:{}'.format(API_KEY,API_PASS).encode('utf-8')).decode('ascii'))
    return json.loads(urlopen(q).read())

def get_full_schedule(league):
    if league == 'nfl':
        type = '2019-playoff'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'full_game_schedule'

    games = msf_request(URL.format(league,type,endpoint))

    return games['fullgameschedule']['gameentry']

def schedule_by_date(schedule):
    games = dict()
    for game in schedule:
        if game['date'] in games:
            games[game['date']] += [game]
        else:
            games[game['date']] = [game]
    return games

def all_teams(league):
    if league == 'nfl':
        type = '2018-regular'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'overall_team_standings'
    teams = msf_request(URL.format(league,type,endpoint))

    return teams['overallteamstandings']['teamstandingsentry']
