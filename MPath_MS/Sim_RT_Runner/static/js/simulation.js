var fetchDataIntervalID;

function start_graphic(db_identifier) {
    graphic.db_identifier = db_identifier;
    graphic.start();
    graphic.iterative_fetch_data([]);
}

function stop_fetching_data() {
    clearInterval(fetchDataIntervalID);
}