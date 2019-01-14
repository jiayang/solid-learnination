team_icons = document.getElementsByClassName('team_icon')

for (var i = 0; i < team_icons.length; i++) {
    var ele = team_icons[i];
    var data = ele.innerHTML.split('/');
    var league = data[1];
    var team = data[0];
    var img = '';
    if (league == 'nba') {
	if (team == 'OKL') {
	    img  = 'http://cdn.nba.net/assets/logos/teams/secondary/web/OKC.svg'
	} else if (team == 'BRO') {
	    img = "http://cdn.nba.net/assets/logos/teams/secondary/web/BKN.svg"
	} else {
	    img = "http://cdn.nba.net/assets/logos/teams/secondary/web/" + team + ".svg";
	}
    } else if (league == 'nfl') {
	img = "https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/" + team + ".svg"
    } else if (league == 'mlb') {
	img = "https://www.mlbstatic.com/team-logos/" + team + ".svg";
    } else {
	img = "https://www-league.nhlstatic.com/images/logos/teams-current-circle/" + team + ".svg";
    }
    ele.innerHTML = '<img class="team_icon" src="' + img + '">';

}
