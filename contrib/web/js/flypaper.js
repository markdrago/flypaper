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
        rows += "<tr>";
        rows += "<td>" + file.score + "</td>";
        rows += "<td>" + file.filename + "</td>";
        rows += "<td>" + file.bugs + "</td>";
        rows += "</tr>";
    }

    var table = $('table#results');
    var tbody = table.find('tbody');
    tbody.empty();
    tbody.append(rows);

    //tell tablesorter that we changed the data underneath it
    table.trigger("update"); 
}
