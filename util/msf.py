from urllib.request import Request,urlopen
import json
import base64



def msf_request(url):
    q = Request(url)
    q.add_header('Authorization', 'Basic ' + base64.b64encode('{}:{}'.format(API_KEY,API_PASS).encode('utf-8')).decode('ascii'))
    return json.loads(urlopen(q).read())

def get_full_schedule(league):
    endpoint = 'full_game_schedule'
    if league == 'nfl':
        type = ['2019-playoff','2018-regular']
        regular = msf_request(URL.format(league,type[0],endpoint))
        playoff = msf_request(URL.format(league,type[1],endpoint))
        return regular['fullgameschedule']['gameentry'] + playoff['fullgameschedule']['gameentry']
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'



    games = msf_request(URL.format(league,type,endpoint))

    return games['fullgameschedule']['gameentry']

def reorder_schedule_by_team(schedule,team):
    games = []
    for game in schedule:
        print(game['homeTeam']['Name'])
        team_name = team.split('-')[1].lower()
        print(team_name)
        awayTeam = ''.join(game['awayTeam']['Name'].lower().split(' '))
        homeTeam = ''.join(game['homeTeam']['Name'].lower().split(' '))
        if homeTeam == team_name or awayTeam == team_name:
            games += [game]
    return games
def reorder_schedule_by_date(schedule):
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
def get_all_player_stats_by_team(league,team):
    if league == 'nfl':
        type = '2018-regular'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'cumulative_player_stats'
    parameters = '?team=' + team
    players = msf_request(URL.format(league,type,endpoint) + parameters)

    return players['cumulativeplayerstats']['playerstatsentry']

keys = ''
if __name__ == '__main__':
    keys = json.loads(open('../data/keys.json','r').read())
else:
    keys = json.loads(open('data/keys.json','r').read())
API_KEY = keys['mysportsfeeds']
API_PASS = keys['msf_password']
URL = 'https://api.mysportsfeeds.com/v1.0/pull/{}/{}/{}.json' # sports type (nba,nfl,nhl,mlb) ; season type ; endpoint
