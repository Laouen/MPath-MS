function exportDataAsCSV(series) {

    // Create csv string
    var csvContent = "data:text/csv;charset=utf-8,";
    csvContent += ['metabolite_id', 'simulation_virtual_time', 'amount'].join(",") + "\r\n";
    for (var i = 0; i < series.length; i++) {
        metaboliteID = series[i].metabolite;
        metaboliteData = series[i].data;
        for (var j = 0; j < metaboliteData.times.length; j++) {
            csvContent += [metaboliteID, metaboliteData.times[j], metaboliteData.serie[j]].join(",") + "\r\n";
        }
    }

    // Download as file
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "mpath_data.csv");
    document.body.appendChild(link); // Required for FF
    link.click();
}