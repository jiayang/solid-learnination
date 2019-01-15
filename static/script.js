team_icons = document.getElementsByClassName('team_icon')

for (var i = 0; i < team_icons.length; i++) {
    var ele = team_icons[i];
    var data = ele.innerHTML.split(';');
    var childs_to_add = [];
    var text_to_add = [];
    for (var j = 0; j < data.length; j++) {

        var args = data[j].split('/');
        var league = args[1];
        var team = args[0];
        var url = '';

        if (league == 'nba') {
    	    if (team == 'OKL') {
    	        url  = 'http://cdn.nba.net/assets/logos/teams/secondary/web/OKC.svg';
    	    } else if (team == 'BRO') {
                url = "http://cdn.nba.net/assets/logos/teams/secondary/web/BKN.svg";
            } else {
                url = "http://cdn.nba.net/assets/logos/teams/secondary/web/" + team + ".svg";
            }
        } else if (league == 'nfl') {
    	    url = "https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/" + team + ".svg";
        } else if (league == 'mlb') {
            url = "https://www.mlbstatic.com/team-logos/" + team + ".svg";
        } else {
            url = "https://www-league.nhlstatic.com/images/logos/teams-current-circle/" + team + ".svg";
        }
        var img = document.createElement("img");
        img.src = url;
        img.className += ' team_icon_img';
        childs_to_add.push(img);
        text_to_add.push(args[2]);
    }
    ele.innerHTML = '';
    console.log(childs_to_add)
    for (var k = 0; k < data.length; k++) {
        ele.appendChild(childs_to_add[k]);
        ele.innerHTML += text_to_add[k] + '<br>'
    }



}
