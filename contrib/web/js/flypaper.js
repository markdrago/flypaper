var RESULTS_LOCATION = "flypaper_results.json";

$(document).ready(function() {

    get_json_via_ajax(RESULTS_LOCATION, update_ui);

});

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

    var table = $('table#results tbody');
    table.empty();
    table.append(rows);
}
