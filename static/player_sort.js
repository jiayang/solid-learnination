var fibonacci = (n) => {
    var first = 0;
    var second = 1;
    for (i = 0; i < n; i++) {
	var temp = second;
	second += first;
	first = temp;
    }
    console.log(first);
    return first;
}

//i is the index of the value to sort the rows by
var row_sort = (rows,sort_col) => {
    new_rows = [];
    for (var i = 1; i < rows.length; i++) {
        new_rows.push([rows[i],sort_col]);
    }
    new_rows.sort(compare);
    return new_rows;
}

var compare = (a,b) => {
    var aVal = a[0].cells[a[1]+1].innerHTML;
    var bVal = b[0].cells[b[1]+1].innerHTML;
    if (!isNaN(aVal) && !isNaN(bVal)) {
        return parseInt(aVal) - parseInt(bVal);
    }
    for (var i = 0; i < Math.min(bVal.length,aVal.length);i++) {
        if (aVal.charAt(i) > bVal.charAt(i)) {
            return 1;
        } else if (aVal.charAt(i) < bVal.charAt(i)){
            return -1;
        }
    }
    return 0;
}

all_stats = ['min','pts','fgm','fga','reb','ast','stl','blk','plsmns']

//Not in a for loop because can't figure out how to reference the iterating value in the for loop within the inner function
document.getElementById(all_stats[0]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,0)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[1]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,1)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[2]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');
    var new_rows = row_sort(rows,2);
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[3]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,3)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[4]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,4)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[5]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,5)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[6]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,6)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[7]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,7)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
document.getElementById(all_stats[8]).addEventListener("click" , function () {
    var tbl = document.getElementById('nba_boxscore')
    var rows = tbl.getElementsByTagName('tr');

    var new_rows = row_sort(rows,8)
    for (var i = 0; i < new_rows.length; i++) {
        rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
    }
});
