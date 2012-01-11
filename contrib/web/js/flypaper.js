var RESULTS_LOCATION = "flypaper_results.json";

$(document).ready(function() {
    prepare_ui();
    get_json_via_ajax(RESULTS_LOCATION, update_ui);
});

function prepare_ui() {
    $("table#results").tablesorter();
}

function get_json_via_ajax(filename, callback) {
    $.ajax({
        type: "GET",
        url: filename,
        dataType: "json",
        success: function(data) {
            callback(data);
        }
    });
}

function update_ui(results) {
    var rows = "";
    for (var i in results.files) {
        var file = results.files[i];
        var score = new Number(file.score);
        rows += "<tr>";
        rows += "<td>" + score.toPrecision(4) + "</td>";
        rows += "<td title=\"" + file.filename + "\">" + shorten_filename(file.filename) + "</td>";
        rows += "<td>" + file.bugs.join(', ') + "</td>";
        rows += "</tr>";
    }

    var table = $('table#results');
    var tbody = table.find('tbody');
    tbody.empty();
    tbody.append(rows);

    //tell tablesorter that we changed the data underneath it
    table.trigger("update"); 
}

function shorten_filename(filename) {
    var reasonable_length = 85;

    //if the full filename isn't that long, just use it
    if (filename.length < reasonable_length) {
        return filename;
    }

    //split the filename up on slashes
    var parts = filename.split('/');

    //try and shorten the name and still include some path info
    var shortname = parts[0];
    if (parts.length > 0) {
        shortname += "/.../" + parts[parts.length - 1];
    }

    //if the name is still too long, just use the basename
    if (shortname.length > reasonable_length && parts.length > 0) {
        shortname = parts[parts.length - 1];
    }

    return shortname;
}
