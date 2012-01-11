var RESULTS_LOCATION = "flypaper_results.json";
var OPTIONS_LOCATION = "options.json";
var PAGE_SIZE = 100;

$(document).ready(function() {
    get_json_via_ajax(OPTIONS_LOCATION,
        function(options) {
            prepare_table();
            get_json_via_ajax(RESULTS_LOCATION,
                function(results) {
                    add_data_rows(results, options, PAGE_SIZE);
                    prepare_more_button(results, options);
                }
            );
        }
    );
});

function prepare_table() {
    //initialize sorting
    $("table#results").tablesorter({
        //disable sorting of the bugs column
        headers: { 2: { sorter: false } }
    });
}

function prepare_more_button(results, options) {
    $('#more').click(function() {
        add_data_rows(results, options, PAGE_SIZE);
    });
}

function get_displayed_rows_count() {
    return $("table#results tr").length;
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

function add_data_rows(results, options, limit) {
    var rows = "";

    //figure out which rows to add
    var start = get_displayed_rows_count();
    var stop = Math.min(start + limit, results.files.length);

    for (var i = start; i < stop; i++) {
        var file = results.files[i];
        var score = new Number(file.score);
        rows += "<tr>";
        rows += "<td>" + score.toPrecision(4) + "</td>";
        rows += "<td title=\"" + file.filename + "\">" + shorten_filename(file.filename) + "</td>";
        rows += "<td>" + get_buglist(file.bugs, options.bugs.linkformat) + "</td>";
        rows += "</tr>";
    }

    var table = $('table#results');
    var tbody = table.find('tbody');
    tbody.append(rows);

    //tell tablesorter that we changed the data underneath it
    table.trigger("update");

    //remove more button if we have shown all
    if (get_displayed_rows_count() >= results.files.length) {
        $('#more').hide();
    }
}

function get_buglist(bugs, linkformat) {
    bugs.sort().reverse();

    //create comma-separated list of bug ids
    var sep = "";
    var buglist = "";
    for (var j in bugs) {
        buglist += sep;
        var bug = bugs[j];

        //optionally create bug ids in to links
        if (linkformat != undefined && linkformat != "") {
            bugtag = "<a href=\"" + linkformat + "\">" + bug + "</a>" ;
            bug = bugtag.replace("{bugid}", bug);
        }
        buglist += bug;
        sep = ", ";
    }

    return buglist;
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
