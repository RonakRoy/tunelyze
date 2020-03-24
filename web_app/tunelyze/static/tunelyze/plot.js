const margin = {
    t: 40,
    r: 30,
    b: 45,
    l: 45,
}
const things = {staticPlot: true, responsive: true};

function bar_marker(secondary) {
    var color;
    if (secondary) {
        color = "#a3bfcc"
    }
    else {
        color = "#778DA9"
    }

    return {
        color: color,
        line: {
            color: '#E0E1DD',
            width: 0.0
        }
    }
}

function histogram_trace(data, min, max, tick_spacing, secondary) {
    return {
        type: 'histogram',
        x: data,

        xbins: {
            start: min,
            end: max,
            size: tick_spacing / 5.0,
        },
        
        marker: bar_marker(secondary)
    }
}

function plot_histogram(feature_name, traces, min, max, tick_spacing) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: {
            text: feature_name,
            font: {
                color: '#E0E1DD'
            }
        },
        showlegend: false,
        barmode: "overlay",
        bargroupgap: 0.25,
        xaxis: {
            dtick: tick_spacing,
            range: [min,max],

            ticklen: 6,
            tickwidth: 1,
            showline: true,
            zeroline: false,

            linewidth: 2,
            color:  '#E0E1DD'
        },
        yaxis: {
            ticklen: 6,
            tickwidth: 1,
            showline: true,

            gridcolor: '#b5b7ae',

            linewidth: 2,
            color:  '#E0E1DD'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: "'Montserrat', 'Helvetica', 'Arial', sans-serif",
            size: 18
        },
        margin: margin,
    }, things)
}

function filtered_histogram(feature_name, filtered_feature_values, feature_values, min, max, tick_spacing) {
    plot_histogram(feature_name, [
        histogram_trace(feature_values[feature_name], min, max, tick_spacing, false),
        histogram_trace(filtered_feature_values[feature_name], min, max, tick_spacing, true)
    ], min, max, tick_spacing)
}

function histogram(feature_name, feature_values, min, max, tick_spacing) {
    plot_histogram(feature_name, [
        histogram_trace(feature_values[feature_name], min, max, tick_spacing),
    ], min, max, tick_spacing)
}



function bar_trace(feature_name, features, categories, secondary) {
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

        marker: bar_marker(secondary)
    }
}

function plot_bar(feature_name, traces) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: {
            text: feature_name,
            font: {
                color: '#E0E1DD'
            }
        },
        showlegend: false,
        barmode: "overlay",
        xaxis: {
            ticklen: 6,
            tickwidth: 1,
            showline: true,
            zeroline: false,

            linewidth: 2,
            color:  '#E0E1DD'
        },
        yaxis: {
            ticklen: 6,
            tickwidth: 1,
            showline: true,

            gridcolor: '#b5b7ae',

            linewidth: 2,
            color:  '#E0E1DD'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: "'Montserrat', 'Helvetica', 'Arial', sans-serif",
            size: 18
        },
        margin: margin
    }, things)
}

function filtered_bar(feature_name, filtered_feature_values, feature_values, categories) {
    plot_bar(feature_name, [
        bar_trace(feature_name, feature_values, categories, false),
        bar_trace(feature_name, filtered_feature_values, categories, true),
    ])
}

function bar(feature_name, feature_values, categories) {
    plot_bar(feature_name, [
        bar_trace(feature_name, feature_values, categories)
    ])
}



function pie_trace(feature_name, features, categories, colors, name, col) {
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
        marker: {
            colors: colors
        },
        textinfo: "label+percent",
        values: values,
        name: name,
        domain: {
            row: 0,
            column: col
        },
    }
}

function plot_pie(num, title, feature_name, traces) {
    Plotly.newPlot(feature_name + "_plot", traces,
    {
        title: {
            text: title,
            font: {
                color: '#E0E1DD'
            }
        },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: "'Montserrat', 'Helvetica', 'Arial', sans-serif",
            size: 18
        },
        margin: {
            t: 40,
            r: 0,
            b: 10,
            l: 0,
        },
        grid: {rows: 1, columns: num}
    }, things)
}

function filtered_pie(feature_name, filtered_features, features, categories) {
    plot_pie(1, feature_name+" (all tracks)", feature_name, [
        pie_trace(feature_name, features, categories, ["#778DA9", "#a3bfcc"], "all tracks", 0)
    ])

    plot_pie(1, feature_name+" (filtered)", "filtered_"+feature_name, [
        pie_trace(feature_name, filtered_features, categories, ["#778DA9", "#a3bfcc"], "filtered", 0),
    ])
}

function pie(feature_name, features, categories) {
    plot_pie(1, feature_name, feature_name, [
        pie_trace(feature_name, features, categories, ["#778DA9", "#a3bfcc"], "tracks", 0)
    ])
}