var options = {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Simulation results'
    },
    subtitle: {
        text: ''
    },
    yAxis: {
        title: {
            text: 'Metabolites amount'
        }
    },
    legend: {
        enabled: true
    }
}

var graphic = {

    series: [],

    last_virtual_time: "00:00:00:000",

    db_identifier: "",

    start: function() {
        graphic.chart = Highcharts.chart('plot', $.extend(true, {}, options));
    },

    iterative_fetch_data: function(data) {
        this.fetch_data_success(data);
        this.fetch_data(this.iterative_fetch_data.bind(this));
    },

    fetch_data: function(onSuccess) {

        console.log("[Graphic] Fetch data");

        $.post(
            '/Sim_RT_Runner/get/simulation_results/',
            JSON.stringify({
                start_virtual_time: this.last_virtual_time,
                db_identifier: this.db_identifier
            }),
            onSuccess
        );
    },

    fetch_data_success: function(data) {
        if (data.length > 0) {
            this.add_data(data);
        }
    },

    add_data: function(data) {
        this.mergeData(data);
        
        var null_prefix_series = [];
        var prefix_times = [];
        if (this.series.length > 0) {
            null_prefix_series = this.series[0].data.times.map(function() {return null});
            prefix_times = $.extend(true, [], this.series[0].data.times);
        }

        var null_suffix_serie = [];
        var suffix_times = [];
        if (data.length > 0) {
            null_suffix_serie = data[0].data.times.map(function() {return null});
            suffix_times = $.extend(true, [], data[0].data.times);
        }

        // Update existent series
        for (var i = 0; i < this.series.length; i++) {
            var found = false;
            for (var j = 0; j < data.length; j++) {
                if (this.series[i].metabolite === data[j].metabolite) {
                    this.series[i].data.times = this.series[i].data.times.concat(data[j].data.times);
                    this.series[i].data.serie = this.series[i].data.serie.concat(data[j].data.serie);
                    found = true;
                    break;
                }
            }

            if (!found) {
                this.series[i].data.serie = this.series[i].data.serie.concat(null_suffix_serie);
                this.series[i].data.times = this.series[i].data.times.concat(suffix_times);
            }

            this.chart.series[i].setData(this.series[i].data.serie, false);
        }

        // Add new series
        for (var j = 0; j < data.length; j++) {
            var new_serie = true;
            for (var i = 0; i < this.series.length; i++) {
                if (this.series[i].metabolite === data[j].metabolite) {
                    new_serie = false;
                    break;
                }
            }

            if (new_serie) {
                if (null_prefix_series.length > 0) {
                    data[j].data.serie = null_prefix_series.concat(data[j].data.serie);
                    data[j].data.times = prefix_times.concat(data[j].data.times);
                }

                this.series.push(data[j]);
                this.chart.addSeries({
                    name: data[j].metabolite,
                    data: data[j].data.serie
                }, false);
            }
        }

        this.chart.redraw();
        this.update_categories();
    },

    update_categories: function() {
        this.chart.xAxis[0].setCategories(this.series[0].data.times, true);
        this.last_virtual_time = this.series[0].data.times[this.series[0].data.times.length - 1];
    },

    mergeData: function(datas) {
        var index = 0;

        while (index < Math.max.apply(null, datas.map(function(d) {return d.data.times.length}))) {


            var current_element = datas[0].data.times[index];
            for(var i = 1; i < datas.length; i++) {
                if (datas[i].data.times[index] < current_element) {
                    current_element = current_element;
                }
            }

            for (var i = 0; i < datas.length; i++) {
                if (datas[i].data.times[index] !== current_element) {
                    datas[i].data.times.splice(index, 0, current_element);
                    datas[i].data.serie.splice(index, 0, null);
                }
            }

            index++;
        }
    }
}