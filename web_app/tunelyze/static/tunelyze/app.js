$(document).ready(function() {
    $("#all_albums").click(function() {
        $(".album").each(function(index) {
            $(this).addClass("selected")
        })
    })

    $("#clear_albums").click(function() {
        $(".album").each(function(index) {
            $(this).removeClass("selected")
        })
    })

    $("#all_playlists").click(function() {
        $(".playlist").each(function(index) {
            $(this).addClass("selected")
        })
    })

    $("#clear_playlists").click(function() {
        $(".playlist").each(function(index) {
            $(this).removeClass("selected")
        })
    })

    $("#showhide_filters").click(function() {
        if ($("#filter_picker").hasClass("hidden")) {
            $("#showhide_filters").html("hide");
        }
        else {
            $("#showhide_filters").html("show");
        }
        $("#filter_picker").toggleClass("hidden")
        $("#filter_summary").toggleClass("hidden")
    })

    //========================================\\
    //==== Feature Filter Interface Setup ====\\
    //========================================\\
    feature_types = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    feature_defs = {
        'danceability':     {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'energy':           {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'key':              {type: 'discrete', options: ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B']},
        'loudness':         {type: 'range', min: -60.0, max: 0.0, tick_spacing: 5.0},
        'mode':             {type: 'discrete', options: ['minor', 'major']},
        'speechiness':      {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'acousticness':     {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'instrumentalness': {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'liveness':         {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'valence':          {type: 'range', min: 0.0, max: 1.0, tick_spacing: 0.1},
        'tempo':            {type: 'range', min: 0.0, max: 250.0, tick_spacing: 25},
    }

    for (var i = 0; i < feature_types.length; i++) {
        const feature = feature_types[i]
        const feature_def = feature_defs[feature]

        if (feature_def.type == "range") {
            const min_val = feature_def.min
            const max_val = feature_def.max

            $("#filter").append(
                "<div class='filter_block' id='" + feature + "_block'>" + 
                    "<div class='slider_block'>" +
                        "<div class='slider_text'>" + 
                            "<div class='min slider_label' id='" + feature + "_min'>" + min_val +"</div>" + 
                            "<div style='flex: 1 0 auto'>" + 
                                "<div class='switch' id='use_" + feature + "_filter'>" +
                                    "<span class='knob'></span>" + 
                                "</div>" +
                                "<div class='title'>" +
                                    "<b>" + feature + "</b>" +
                                "</div>" + 
                            "</div>" + 
                            "<div class='max slider_label' id='" + feature + "_max'>" + max_val +"</div>" + 
                        "</div>" + 
                        "<div class='slider' id='" + feature + "_slider'></div>" + 
                    "</div>" +
                "</div>"
            )

            $("#use_" + feature + "_filter").click(function() {
                $(this).toggleClass("on")
                $("#"+feature+"_block").toggleClass("on")
            })

            $("#" + feature + "_slider").slider({
                range: true,
                min: feature_def.min,
                max: feature_def.max,
                step: feature_def.tick_spacing / 5,
                values: [feature_def.min, feature_def.max],
                slide: function(event, ui) {
                    $("#" + feature + "_min").html(ui.values[0])
                    $("#" + feature + "_max").html(ui.values[1])
                }
            })
        }
        else if (feature_def.type == "discrete") {
            var in_checks = ""
            var options = feature_def.options
            for (var j = 0; j < options.length; j++) {
                in_checks +=  "<div style='display: inline-block; margin: 0px 4px'><input type='checkbox' checked='true' class='" + feature + "_options' id='" + feature + "_" + options[j] + "' class='filter'> " + options[j] + "</div>"
            }

            $("#filter").append(
                "<div class='filter_block' id='" + feature + "_block'>" + 
                    "<div class='picker_block'>" +
                        "<div style='display: flex; align-items: center; margin-bottom: 4px'>" +
                            "<div class='switch' id='use_" + feature + "_filter'>" +
                                "<span class='knob'></span>" + 
                            "</div>" +
                            "<div class='title'>" +
                                "<b>&nbsp" + feature + "</b>" +
                            "</div>" + 
                        "</div>" + 
                        "<div>" +
                            in_checks +
                        "</div>" + 
                    "</div>" +
                "</div>"
            )

            $("#use_" + feature + "_filter").click(function() {
                $(this).toggleClass("on")
                $("#"+feature+"_block").toggleClass("on")
            })
        }
    }

    function process_features(tracks) {
        var feature_values = {}

        for (var i = 0; i < feature_types.length; i++) {
            feature_values[feature_types[i]] = []
        }

        for (var i = 0; i < tracks.length; i++) {
            track_features = tracks[i]["features"]
            for (var feature in track_features) {
                if (feature != "type") {
                    feature_values[feature][i] = track_features[feature]
                }
            }
        }

        return feature_values
    }

    var tracks
    var feature_values

    var filtered_tracks
    var filtered_feature_values

    //=======================================\\
    //======== Loading Track Sources ========\\
    //=======================================\\
    $("#saved").click(function() {
        $(this).toggleClass('selected')
    })

    $.ajax({url: "../get_saved_albums/", success: function(result) {
        $("#albums").html("")
        albums = result["albums"]
        for (var i = 0; i < albums.length; i++) {
            $("#albums").append(
                "<div class='album source clickable hover_animate' id='" + albums[i]["id"] + "'>" + 
                    "<img class='art hover_animate' src='" + albums[i]["art_url"] + "'></img>" + 
                    "<div><b>" + albums[i]["name"] + "</b><br>" + albums[i]["artists_str"] + "</div>" +
                "</div>"
            )
        }

        $(".album").each(function(index) {
            $(this).click(function() {
                $(this).toggleClass('selected')
            })
        })
    }})
    $.ajax({url: "../get_playlists/", success: function(result) {
        $("#playlists").html("")
        playlists = result["playlists"]
        for (var i = 0; i < playlists.length; i++) {
            $("#playlists").append(
                "<div class='playlist source clickable hover_animate' id='" + playlists[i]["id"] + "'>" + 
                    "<img class='art hover_animate' src='" + playlists[i]["art_url"] + "'></img>" + 
                    "<div><b>" + playlists[i]["name"] + "</b><br>" + playlists[i]["owner"] + "</div>" +
                "</div>"
            )
        }

        $(".playlist").each(function(index) {
            $(this).click(function() {
                $(this).toggleClass('selected')
            })
        })
    }})

    //========================================\\
    //============= Track Loader =============\\
    //========================================\\
    $("#load_tracks").click(function() {
        saved = $("#saved").hasClass('selected')

        album_ids = ""
        $(".album").each(function(index) {
            if ($(this).hasClass('selected')) {
                album_ids += $(this).attr('id') + ","
            }
        })


        playlist_ids = ""
        $(".playlist").each(function(index) {
            if ($(this).hasClass('selected')) {
                playlist_ids += $(this).attr('id') + ","
            }
        })

        $("#tracks").html("<div class='track'><i>Loading tracks...</i></div>")
        $.ajax({url: "../get_tracks/?saved=" + saved + "&albums=" + album_ids + "&playlists=" + playlist_ids,
            error: onError,
            success: function(result) {
                $("#tracks").html("")

                tracks = result["tracks"]
                for (var i = 0; i < tracks.length; i++) {
                    $("#tracks").append(
                        "<div class='track' id='" + tracks[i]["id"] + "'>" + 
                            "<img class='art hover_animate' src='" + tracks[i]["art_url"] + "'></img>" +
                            "<div><b>" + tracks[i]["name"] + "</b><br>" + tracks[i]["artists_str"] + "</div>" +
                        "</div>"
                    )
                }
                feature_values = process_features(tracks)

                $("#feature_prompt").css("display", "none")
                for (var i = 0; i < feature_types.length; i++) {
                    var feature = feature_types[i]
                    var feature_def = feature_defs[feature]

                    if (feature_def.type == "range") {
                        histogram(feature, feature_values, feature_def.min, feature_def.max, feature_def.tick_spacing)
                    }
                    else if (feature == 'key') {
                        bar('key', feature_values, feature_def.options)
                    }
                    else if (feature == 'mode') {
                        pie('mode', feature_values, feature_def.options)
                    }
                }

                filtered_tracks = []
                filtered_feature_values = []

                $("#playlist_prompt").html("Apply some filters to start generating playlists!")
                $("#playlist").css("display", "none")
            }
        })
    })

    //========================================\\
    //============ Filter Applier ============\\
    //========================================\\
    $("#apply_filters").click(function() {
        var summary = "The following filters are enabled: "

        filtered_tracks = tracks.slice()
        var track_buffer = []

        for (var i = 0; i < feature_types.length; i++) {
            var feature = feature_types[i]
            var feature_def = feature_defs[feature]

            if ($("#use_" + feature + "_filter").hasClass('on') == false) {
                continue
            }

            summary += "<b>" + feature + "</b> "

            if (feature_def.type == 'range') {
                min_val = $("#" + feature + "_min").html()
                max_val = $("#" + feature + "_max").html()

                for (var j = 0; j < filtered_tracks.length; j++) {
                    var track = filtered_tracks[j]
                    var feature_value = track["features"][feature]

                    if (feature_value >= min_val && feature_value <= max_val) {
                        track_buffer.push(track)
                    }
                }

                summary += "is between " + min_val + " and " + max_val + ", "
            }
            else {
                allowed_options = []
                $("." + feature + "_options").each(function(index) {
                    if ($(this).prop('checked')) {
                        allowed_options.push($(this).attr('id').substring(feature.length + 1))
                    }
                })

                summary += "is one of (" + allowed_options + "), "

                for (var j = 0; j < filtered_tracks.length; j++) {
                    var track = filtered_tracks[j]
                    var feature_value = track["features"][feature]

                    if (allowed_options.indexOf(feature_value) != -1) {
                        track_buffer.push(track)
                    }
                }
            }

            filtered_tracks = track_buffer.slice()
            track_buffer = []
        }

        if (summary == "The following filters are enabled: ") {
            summary = "No filters are currently enabled."
        }
        else {
            summary = summary.slice(0,-2)
        }
        $("#filter_summary").html(summary)

        $("#showhide_filters").html("show");

        $("#filter_picker").addClass("hidden")
        $("#filter_summary").removeClass("hidden")

        $('.track').each(function(index) {
            $(this).addClass('filtered_out')
        })

        for (var i = 0; i < filtered_tracks.length; i++) {
            $('#' + filtered_tracks[i]['id']).removeClass('filtered_out')
        }

        filtered_feature_values = process_features(filtered_tracks)
        for (var i = 0; i < feature_types.length; i++) {
            var feature = feature_types[i]
            var feature_def = feature_defs[feature]

            if (feature_def.type == "range") {
                filtered_histogram(feature, filtered_feature_values, feature_values, feature_def.min, feature_def.max, feature_def.tick_spacing)
            }
            else if (feature == 'key') {
                filtered_bar('key', filtered_feature_values, feature_values, feature_def.options)
            }
            else if (feature == 'mode') {
                filtered_pie('mode', filtered_feature_values, feature_values, feature_def.options)
            }
        }

        $("#playlist_prompt").html("Of the original <b>" + tracks.length + " tracks,</b> your filters produced <b>"  + filtered_tracks.length + " tracks.</b>");
        $("#playlist").css("display", "block");

        //========================================\\
        //=========== Playlist Creator ===========\\
        //========================================\\
        $("#make_plist").click(function() {
            name = $("#plist_name").prop('value')

            if (name == "") {
                $("#plist_result").html("ERROR: Your playlist needs a name!")
                return
            }
            $("#plist_result").html("<i>Creating playlist </i>" + name + "<i>...</i>")

            track_ids = ""
            for (var i = 0; i < filtered_tracks.length; i++) {
                track_ids += filtered_tracks[i]['id'] + ","
            }

            $.ajax({url: "../make_playlist/?name=" + name + "&tracks=" + track_ids,
                error: onError,
                success: function(result) {
                    $("#plist_result").html("Your playlist has been created! View <a target='_blank' href='https://open.spotify.com/playlist/" + result['id'] + "'>" + name + " on Spotify.</a>")
                }
            })
        })
    })
})

$("body").ready(function() {
    $("#main_content").css("max-height", $(window).height() - $("#header").height() - 48)
})

$(window).resize(function() {
    $("#main_content").css("max-height", $(window).height() - $("#header").height() - 48)
})

function onError(jqXHR, textStatus, errorThrown) {
    if (jqXHR.responseText == "Spotify authorization failed.") {
        const response = confirm("Unfortunately, tunelyze lost Spotify authorization in your browser. Click OK to reload the page.")

        if (response == true) {
            location.reload(true)
        }
    }
    else {
        alert("An unknown error has occurred.")
    }
}