
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

function determine_replication_state_image(status_code,
                                           stratum0,
                                           stratum1,
                                           last_revision) {
    var small    = (arguments.length == 5) ? arguments[4] : false;
    var img_name = "fail.png";
    // avoid flickering due to out of sync caches
    var revision = (stratum1.revision >= last_revision)
                        ? stratum1.revision
                        : last_revision;

    if (status_code != 'ok') {
        return _mangle_status_image_name("fail.png", small);
    }

    if (stratum1.replicating == "True") {
        return _mangle_status_image_name("spinner.gif", small);
    }

    if (revision == stratum0.revision) {
        return _mangle_status_image_name("tick.png", small);
    }

    if (revision + 1 == stratum0.revision) {
        return _mangle_status_image_name("tick_degraded.png", small);
    }

    return _mangle_status_image_name("cross.png", small);
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
