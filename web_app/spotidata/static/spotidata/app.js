$(document).ready(function() {
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
        var feature = feature_types[i]
        var feature_def = feature_defs[feature]

        if (feature_def.type == "range") {
            $("#filter").append(
                "<div>" +
                    "<input type='checkbox' id='use_" + feature + "_filter' class='filter' /> <b>" + feature + "</b> &nbsp &nbsp &nbsp &nbsp" +
                    "min: <input type='text' id='" + feature + "_min' value='" + feature_def.min + "' /> &nbsp &nbsp" +
                    "max: <input type='text' id='" + feature + "_max' value='" + feature_def.max + "' />" + 
                "</div>"
            )
        }
        else if (feature_def.type == "discrete") {
            var in_checks = ""
            var options = feature_def.options
            for (var j = 0; j < options.length; j++) {
                in_checks +=  "<input type='checkbox' class='" + feature + "_options' id='" + feature + "_" + options[j] + "' class='filter' /> " + options[j] + " &nbsp &nbsp"
            }

            $("#filter").append(
                "<div>" +
                    "<input type='checkbox' id='use_" + feature + "_filter' class='filter' /> <b>" + feature + "</b> &nbsp &nbsp &nbsp &nbsp" +
                    in_checks + 
                "</div>"
            )
        }
    }
    $("#filter").append("<button id='apply_filters'>Apply Filters</button>")

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

    //=======================================\\
    //======== Loading Track Sources ========\\
    //=======================================\\
    $.ajax({url: "../get_saved_albums/", success: function(result) {
        $("#albums").html("")
        albums = result["albums"]
        for (var i = 0; i < albums.length; i++) {
            $("#albums").append(
                "<input type='checkbox' class='album' id='" + albums[i]["id"] + "'><b>" + albums[i]["name"] + "</b><br>" + albums[i]["artists_str"] + "</input><br>"
            )
        }
    }})
    $.ajax({url: "../get_playlists/", success: function(result) {
        $("#playlists").html("")
        playlists = result["playlists"]
        for (var i = 0; i < playlists.length; i++) {
            $("#playlists").append(
                "<input type='checkbox' class='playlist' id='" + playlists[i]["id"] + "'><b>" + playlists[i]["name"] + "</b></input><br>"
            )
        }
    }})

    //========================================\\
    //============= Track Loader =============\\
    //========================================\\
    var tracks
    var feature_values
    $("#load_tracks").click(function() {
        saved = $("#saved_tracks").prop('checked')

        album_ids = ""
        $(".album").each(function(index) {
            if ($(this).prop('checked')) {
                album_ids += $(this).attr('id') + ","
            }
        })


        playlist_ids = ""
        $(".playlist").each(function(index) {
            if ($(this).prop('checked')) {
                playlist_ids += $(this).attr('id') + ","
            }
        })

        $("#tracks").html("<i>Loading tracks...</i>")
        $.ajax({url: "../get_tracks/?saved=" + saved + "&albums=" + album_ids + "&playlists=" + playlist_ids, success: function(result) {
            $("#tracks").html("")

            tracks = result["tracks"]
            for (var i = 0; i < tracks.length; i++) {
                $("#tracks").append(
                    "<li class='track' id='" + tracks[i]["id"] + "'><b>" + tracks[i]["name"] + "</b><br>" + tracks[i]["artists_str"] + "</li>"
                )
            }
            feature_values = process_features(tracks)

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
        }})
    })

    //========================================\\
    //============ Filter Applier ============\\
    //========================================\\
    var filtered_tracks
    $("#apply_filters").click(function() {
        filtered_tracks = tracks.slice()
        var track_buffer = []

        for (var i = 0; i < feature_types.length; i++) {
            var feature = feature_types[i]
            var feature_def = feature_defs[feature]

            if ($("#use_" + feature + "_filter").prop('checked') == false) {
                continue
            }

            if (feature_def.type == 'range') {
                min_val = $("#" + feature + "_min").prop('value')
                max_val = $("#" + feature + "_max").prop('value')

                for (var j = 0; j < filtered_tracks.length; j++) {
                    var track = filtered_tracks[j]
                    var feature_value = track["features"][feature]

                    if (feature_value >= min_val && feature_value <= max_val) {
                        track_buffer.push(track)
                    }
                }
            }
            else {
                allowed_options = []
                $("." + feature + "_options").each(function(index) {
                    if ($(this).prop('checked')) {
                        allowed_options.push($(this).attr('id').substring(feature.length + 1))
                    }
                })

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

        $("#playlist").html(
            "Playlist Name: <input type='text' id='plist_name' /> <button id='make_plist'>Create Playlist</button>" +
            "<div id='plist_result'></div>"
        )

        //========================================\\
        //=========== Playlist Creator ===========\\
        //========================================\\
        $("#make_plist").click(function() {
            $("#plist_result").html("<i>Creating...</i>")

            name = $("#plist_name").prop('value')
            track_ids = ""
            for (var i = 0; i < filtered_tracks.length; i++) {
                track_ids += filtered_tracks[i]['id'] + ","
            }

            $.ajax({url: "../make_playlist/?name=" + name + "&tracks=" + track_ids, success: function(result) {
                $("#plist_result").html("Your playlist has been created! View <a href='https://open.spotify.com/playlist/" + result['id'] + "'>" + name + " on Spotify.</a>")
            }})
        })
    })
})