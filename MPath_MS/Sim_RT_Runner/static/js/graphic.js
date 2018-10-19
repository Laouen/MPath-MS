function symbol(series) {
    if (series.symbol === undefined) {
        return '●';
    }

    switch ( series.symbol ) {
        case 'circle': return '●';
        case 'diamond': return '♦';
        case 'square': return '■';
        case 'triangle': return '▲';
        case 'triangle-down': return '▼';
    }
}

function formatter() {
    return this.series.xAxis.userOptions.title.text + ' ' + this.x
        + '<br/>' + '<span style="color:' + this.series.color + '">' + symbol(this.series) + '</span>' + ' '
        + this.series.name + ': <b>' + this.y + '<b>';
}

var graphic = {

    settings: {
        chart: {type: 'area'},
        title: {text: 'Simulation results for model '},
        subtitle: {text: ''},
        yAxis: {title: {text: 'Metabolite amount'}},
        xAxis: {title: {text: 'Time'}},
        tooltip: {formatter: formatter},
    },

    start: function() {
        //Highcharts.setOptions(graphic.options);
        graphic.chart = Highcharts.chart('plot', $.extend(true, {}, graphic.settings));
    },

    add_serie_to_plot: function(data) {
        console.log("Plotting new serie in chart");

        graphic.chart.addSeries({
            data: data.amounts,
            name: data.specie
        });
    },
}