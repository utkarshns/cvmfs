
function _mangle_status_image_name(img_name, small) {
    var result = ""
    if (small) {
        var tokens = img_name.match(/^(.*)(\.[a-z]{3})$/);
        var base   = tokens[1];
        var ext    = tokens[2];
        result += base + "_small" + ext;
    } else {
        result = img_name;
    }
    return result;
}

function determine_replication_state_image(stratum0, stratum1) {
    // parse (optional) third argument
    var small = (arguments.length == 3) ? arguments[2] : false;

    // threshold definitions
    var max_time_offset     = 3600000; // one hour
    var max_revision_offset = 5;

    // if the repository is in the state of replicating, we show
    // a spinner and nothing else...
    if (stratum1.replicating == "True") {
        return _mangle_status_image_name("spinner.gif", small);
    }

    // parse 'last modified' timestamps
    var t_now      = new Date();
    var t_stratum0 = new Date(stratum0.last_modified);
    var t_stratum1 = new Date(stratum1.last_modified);

    // check if the Stratum1 is more than 'max_time_offset' behind the Stratum0
    // this would mean a significant degradation of service
    if (t_stratum0 - t_stratum1 > 0 && t_now - t_stratum0 >= max_time_offset) {
        return _mangle_status_image_name("cross.png", small);
    }

    // check if the Stratum1's revision number lacks far behind the Stratum0's
    // which would indicate a high degradation of service as well
    if (stratum0.revision - stratum1.revision >= max_revision_offset) {
        return _mangle_status_image_name("cross.png", small);
    }

    // if neither the revision nor the 'last_modified' time lack far behind but
    // the Stratum1 is also not on the latest revision, we show a degraded sign
    // Note that this is no critial situation, just for indication...
    if (stratum0.revision != stratum1.revision) {
        return _mangle_status_image_name("tick_degraded.png", small);
    }

    // if all the above degradation checks did not jump in the Stratum1 is con-
    // sidered to be at full health
    return _mangle_status_image_name("tick.png", small);
}

function filter_cache_flickering(state_info, stratum1) {
    var effective_stratum1 = stratum1;

    // update persistent state info when revision has increased
    // this fights flickering due to out of sync caches
    if (state_info.last_stratum1 === undefined) {
        state_info.last_stratum1 = stratum1;
    }
    if (state_info.last_stratum1.revision < stratum1.revision) {
        state_info.last_stratum1 = stratum1;
    } else if (state_info.last_stratum1.revision > stratum1.revision) {
        effective_stratum1 = state_info.last_stratum1; // flicker occured...
    }

    return effective_stratum1;
}

function compare_json(j1, j2) {
    var k1 = Object.keys(j1).sort();
    var k2 = Object.keys(j2).sort();
    if (k1.length != k2.length) return false;
    for (var i = 0; i < k1.length; ++i) {
        if (k1[i] != k2[i]) return false;                        // key name
        if (typeof j1[k1[i]] != typeof j2[k2[i]]) return false;  // value type
        if (typeof j1[k1[i]] == 'object') {                      // recursion
            if(!compare_json(j1[k1[i]],j2[k2[i]])) return false; // deep compare
        }
        else if (j1[k1[i]] != j2[k2[i]]) return false;           // value
    }
    return true;
}

function update_retina_image(img_object) {
    var is_retina = img_object.attr("src").match(/^(.*)@2x(\..*)$/);
    if (is_retina) {
        img_object.attr("src", is_retina[1] + is_retina[2]);
    }
    new RetinaImage(img_object[0])
}

function replace_image(img_object, new_img_filename) {
    var base = img_object.attr("src").match(/([^\.]+\/)[^\/]+/)[1];
    img_object.attr("src", base + new_img_filename)
    update_retina_image(img_object);
}

function leaky_update(url, min_refresh_rate, user_data, success_clb, fail_clb) {
    var old_json    = (arguments.length > 5) ? arguments[5] : null;
    var water_drops = (arguments.length > 6) ? arguments[6] : 0;

    $.getJSON(url)
        .done(function(json_data) {
            if (!old_json || !compare_json(old_json, json_data)) {
                water_drops = 0;
                user_data = success_clb(user_data, json_data);
            } else {
                ++water_drops;
            }

            var next_update = Math.min(1000 * Math.pow(2, water_drops),
                                       1000 * min_refresh_rate);
            setTimeout(function() {
                           leaky_update(url,
                                        min_refresh_rate,
                                        user_data,
                                        success_clb,
                                        fail_clb,
                                        json_data,
                                        water_drops);
                       }, next_update);
        })

        .fail(function(data) {
            fail_clb(user_data, data);
        });
}

function format_timestamp(iso_timestamp) {
    var date_obj = new Date(iso_timestamp)
    return date_obj.toLocaleDateString() + " " + date_obj.toLocaleTimeString();
}
