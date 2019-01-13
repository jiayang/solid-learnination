from urllib.request import Request,urlopen
import json
import base64



def msf_request(url):
    '''Wrapper for requesting a URL from MySportsFeeds'''
    q = Request(url)
    q.add_header('Authorization', 'Basic ' + base64.b64encode('{}:{}'.format(API_KEY,API_PASS).encode('utf-8')).decode('ascii'))
    return json.loads(urlopen(q).read())


def get_full_schedule(league):
    '''Get the full schedule for an entire league. NFL returns playoff and regular season games.'''
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
    '''Returns a list of the games within the schedule being played by specified team'''
    games = []
    for game in schedule:
        team_name = team.split('-')[1].lower()
        awayTeam = ''.join(game['awayTeam']['Name'].lower().split(' '))
        homeTeam = ''.join(game['homeTeam']['Name'].lower().split(' '))
        if homeTeam == team_name or awayTeam == team_name:
            games += [game]
    return games

def reorder_schedule_by_date(schedule):
    '''Returns a dictionary of the games within the schedule, ordered by dates'''
    games = dict()
    for game in schedule:
        if game['date'] in games:
            games[game['date']] += [game]
        else:
            games[game['date']] = [game]
    return games

def all_teams(league):
    '''Returns a list of all the teams in a league'''
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
    '''Returns a list of all the players' stats in a specific team'''
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

def get_all_players_by_team(league,team):
    '''Returns a list of all the players in a specific team with their images'''
    if league == 'nfl':
        type = '2018-regular'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'active_players'
    parameters = '?team=' + team
    players = msf_request(URL.format(league,type,endpoint) + parameters)

    return players['activeplayers']['playerentry']

def get_boxscore(league,game_id):
    '''Returns the boxscore of a game'''
    if league == 'nfl':
        type = '2019-playoff'
    if league == 'nba' or league == 'nhl':
        type = '2018-2019-regular'
    if league == 'mlb':
        type = '2019-regular'

    endpoint = 'game_boxscore'
    parameters = '?gameid=' + game_id
    try:
        boxscore = msf_request(URL.format(league,type,endpoint) + parameters)
    except:
        boxscore = None
    if boxscore == None and league == 'nfl':
        try:
            boxscore = msf_request(URL.format(league,'2018-regular',endpoint) + parameters)
        except:
            boxscore = None
    if boxscore == None:
        return None
    nb = dict()
    awayTeam = ''.join(boxscore['gameboxscore']['game']['awayTeam']['Name'].lower().split(' '))
    homeTeam = ''.join(boxscore['gameboxscore']['game']['homeTeam']['Name'].lower().split(' '))
    nb[awayTeam] = boxscore['gameboxscore']['awayTeam']
    nb['awayTeam'] = nb[awayTeam]
    nb['awayName'] = boxscore['gameboxscore']['game']['awayTeam']['City'] + ' ' + boxscore['gameboxscore']['game']['awayTeam']['Name']
    nb[homeTeam] = boxscore['gameboxscore']['homeTeam']
    nb['homeTeam'] = nb[homeTeam]
    nb['homeName'] = boxscore['gameboxscore']['game']['homeTeam']['City'] + ' ' + boxscore['gameboxscore']['game']['homeTeam']['Name']
    return nb



keys = ''
if __name__ == '__main__':
    keys = json.loads(open('../data/keys.json','r').read())
else:
    keys = json.loads(open('data/keys.json','r').read())
API_KEY = keys['mysportsfeeds']
API_PASS = keys['msf_password']
URL = 'https://api.mysportsfeeds.com/v1.0/pull/{}/{}/{}.json' # sports type (nba,nfl,nhl,mlb) ; season type ; endpoint
