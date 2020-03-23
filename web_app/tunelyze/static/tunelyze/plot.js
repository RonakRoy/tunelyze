const margin = {
    t: 45,
    r: 20,
    b: 30,
    l: 30,
}

function histogram_trace(data, min, max, tick_spacing) {
    return {
        type: 'histogram',
        x: data,

        xbins: {
            start: min,
            end: max,
            size: tick_spacing / 5.0,
        },
        
        marker: {
            line: {
                width: 1.0
            }
        }
    }
}

function plot_histogram(feature_name, traces, min, max, tick_spacing) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: feature_name,
        showlegend: false,
        barmode: "overlay",
        bargroupgap: 0,
        xaxis: {
            dtick: tick_spacing,
            range: [min,max],

            ticklen: 5,
            tickwidth: 1,
            showline: true,
            zeroline: false,
        },
        yaxis: {
            ticklen: 0,
            tickwidth: 1,
            showline: true,
        },
        margin: margin,
    }, {displayModeBar: false})
}

function filtered_histogram(feature_name, filtered_feature_values, feature_values, min, max, tick_spacing) {
    plot_histogram(feature_name, [
        histogram_trace(feature_values[feature_name], min, max, tick_spacing),
        histogram_trace(filtered_feature_values[feature_name], min, max, tick_spacing)
    ], min, max, tick_spacing)
}

function histogram(feature_name, feature_values, min, max, tick_spacing) {
    plot_histogram(feature_name, [
        histogram_trace(feature_values[feature_name], min, max, tick_spacing),
    ], min, max, tick_spacing)
}



function bar_trace(feature_name, features, categories) {
    values = []
    for (var i = 0; i < categories.length; i++) {
        values[i] = 0
    }
    for (var i = 0; i < features[feature_name].length; i++) {
        values[categories.indexOf(features[feature_name][i])] += 1
    }

    return {
        type: 'bar',
        x: categories,
        y: values,

        marker: {
            line: {
                width: 1.0
            }
        }
    }
}

function plot_bar(feature_name, traces) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: feature_name,
        showlegend: false,
        barmode: "overlay",
        xaxis: {
            ticklen: 5,
            tickwidth: 1,
            showline: true,
            zeroline: false,
        },
        yaxis: {
            ticklen: 0,
            tickwidth: 1,
            showline: true,
        },
        margin: margin
    }, {displayModeBar: false})
}

function filtered_bar(feature_name, filtered_feature_values, feature_values, categories) {
    plot_bar(feature_name, [
        bar_trace(feature_name, feature_values, categories),
        bar_trace(feature_name, filtered_feature_values, categories),
    ])
}

function bar(feature_name, feature_values, categories) {
    plot_bar(feature_name, [
        bar_trace(feature_name, feature_values, categories)
    ])
}



function pie_trace(feature_name, features, categories, name, col) {
    values = []
    for (var i = 0; i < categories.length; i++) {
        values[i] = 0
    }
    for (var i = 0; i < features[feature_name].length; i++) {
        values[categories.indexOf(features[feature_name][i])] += 1
    }

    return {
        type: 'pie',
        labels: categories,
        textinfo: "label+percent",
        values: values,
        name: name,
        domain: {
            row: 0,
            column: col
        },
    }
}

function plot_pie(num, feature_name, traces) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: feature_name,
        showlegend: false,
        margin: margin,
        grid: {rows: 1, columns: num}
    }, {displayModeBar: false})
}

function filtered_pie(feature_name, filtered_features, features, categories) {
    plot_pie(2, feature_name, [
        pie_trace(feature_name, filtered_features, categories, "filtered", 1),
        pie_trace(feature_name, features, categories, "all tracks", 0)
    ])
}

function pie(feature_name, features, categories) {
    plot_pie(1, feature_name, [
        pie_trace(feature_name, features, categories, "tracks", 0)
    ])
}