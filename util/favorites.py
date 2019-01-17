def organize_by_league(favs):
    '''organizes favorites based on league'''
    d = {
        'nba' : [],
        'nfl' : [],
        'nhl' : [],
        'mlb' : []
    }
    for fav in favs:
        d[fav[0].split('/')[1]] += [fav]
    return d

def organize_by_team(favs):
    '''organizes favorites by team'''
    d = dict()
    for fav in favs:
        d[fav[0].split('/')[0]] = [fav]
    return d
