team_icons = document.getElementsByClassName('team_icon')

for (var i = 0; i < team_icons.length; i++) {
    var ele = team_icons[i];
    var data = ele.innerHTML.split(';');
    var childs_to_add = [];
    for (var j = 0; j < data.length; j++) {
        var args = data[j].split('/');
        var league = args[1];
        var team = args[0];
        var team2 = args[2].split(' ').join('-').split('.').join('').toLowerCase();
        var name = args[0].split(' ').join('');
        var city = args[2].substring(0,args[2].length -  args[0].length);
        var team3 = city.split(' ').join('')  + '_' +  name;
        team3 = team3.split('.').join('')
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
            if (team3 == 'Toronto_BlueJays') {
                team3 = 'Toronto_Blue_Jays';
            } else if (team3 == 'Chicago_WhiteSox') {
                team3 = 'Chicago_White_Sox';
            }
            url = "http://www.capsinfo.com/images/MLB_Team_Logos/" + team3 + ".png";
        } else {
            url = "https://i.logocdn.com/nhl/2018/" + team2 + ".svg";
        }
        var anchor = document.createElement("A");
        if (league == 'nba' || league == 'nfl') {
            var s = args[2];
            s = s.split('');
            s.splice(s.lastIndexOf(' '),1,'-');
            s = s.join('');
            anchor.href = "/" + league + "/team/" + s;
        } else {
            anchor.href = "/" + league + "/team/" + city.split(' ').join('')  + '-' +  name;
        }
        var img = document.createElement("img");
        img.src = url;
        img.className += ' team_icon_img';

	    anchor.appendChild(img);
        anchor.innerHTML+=(args[2] + '<br>');
        childs_to_add.push(anchor);

    }
    ele.innerHTML = '';
    for (var k = 0; k < data.length; k++) {
        ele.appendChild(childs_to_add[k]);
    }



}

var elemfxn = (e) =>{
    e.addEventListener("click" , function(){
      modal.style.display = "block";
    });
}

var list = document.getElementsByClassName("nav-link");
var e = list[2]
elemfxn(e);


// Get the modal
var modal = document.getElementById('myModal');


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
