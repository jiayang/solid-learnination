//Sorts the DOM tablerow elements by the innerhtml of a specified column
var row_sort = (rows,sort_col) => {
    new_rows = [];
    for (var i = 1; i < rows.length; i++) {
        new_rows.push([rows[i],sort_col]);
    }
    new_rows.sort(compare);
    return new_rows;
}

//Comparing function for the sort used in row_sort(), compares two rows by their inner htmls
var compare = (a,b) => {
    var aVal = a[0].cells[a[1]].innerHTML;
    var bVal = b[0].cells[b[1]].innerHTML;
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

all_stats = ['player','min','pts','fgm','fga','reb','ast','stl','blk','plsmns']

states = ['↑','↓']

for (var i = 0; i < 20; i++) {
    document.getElementById(all_stats[i % 10] + Math.floor(i/10)).addEventListener("click" , function (){
        var tbl = this.parentNode.parentNode //TABLE
        var rows = tbl.getElementsByTagName('tr');
        var new_rows = row_sort(rows,parseInt(this.cellIndex))

        if (this.innerHTML[this.innerHTML.length-1] == '↑') {
            new_rows = new_rows.reverse()
            this.innerHTML = this.innerHTML.substring(0,this.innerHTML.length-1) + '↓'
        } else {
            this.innerHTML = this.innerHTML.substring(0,this.innerHTML.length-1) + '↑'
        }

        for (var i = 0; i < new_rows.length; i++) {
            rows[0].parentNode.insertBefore(new_rows[i][0], rows[0].nextSibling);
        }
        for (var i = 0; i < rows[0].cells.length; i++) {
            if (rows[0].cells[i] != this) {
                rows[0].cells[i].innerHTML = rows[0].cells[i].innerHTML.replace('↑','').replace('↓','')
            }
        }
    });
}
