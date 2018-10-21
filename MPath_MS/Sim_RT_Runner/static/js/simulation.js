var fetchDataIntervalID;

function start_graphic(db_identifier, running) {
    graphic.db_identifier = db_identifier;
    graphic.start();

    if (running) {
        graphic.iterative_fetch_data([]);
    } else {
        graphic.fetch_data(graphic.fetch_data_success.bind(graphic));
    }
}

function stop_fetching_data() {
    clearInterval(fetchDataIntervalID);
}