
/*
var employees = [
    {
        "name": "Admin",
        "id": 1,
        "email": "admin@restaurant.com",
        "hours_limit": 0,
        "role_preferences": {
            "Dishwasher": {
                "id": 1,
                "priority": 1.0,
                "gm_priority": 1.0
            },
        }
        "availability": [
            {
                "day_of_week": 0, // 0 is Monday
                "start_date": "2022-01-08 00:00:00",
                "end_date": "2023-01-08 00:00:00",
                "start_time" : 540, // minutes since midnight
                "end_time": 1020, // minutes since midnight
                "priority": 1.0, // lower numbers higher priority
                "note": "None"
            },
        ]
    }
];

var shifts = [
    {
        "id": 1,
        "day_of_week": 0, // 0 is Monday
        "start_date": "2022-01-03 00:00:00",
        "end_date": "2023-01-03 00:00:00",
        "start_time" : 540, // minutes since midnight
        "end_time": 1020, // minutes since midnight
        "priority": 1.0, // lower numbers higher priority
        "roles" : [
            {
                "role": "Dishwasher",
                "id": "1",
                "number": 2 // number of people needed for this role
            }
        ]
    }
];
*/

/*
    Shifts can be overlapping.
    Find the
*/

function parse_date(date_string) {
    var parts = date_string.match(/(\d+)/g);
    return new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
}

function days_between_dates(d1, d2) {
    return Math.round(Math.abs(d2.getTime() - d1.getTime()) / (1000 * 60 * 60 * 24));
}

function shift_range(shift) {
    return days_between_dates(parse_date(shift.start_date), parse_date(shift.end_date));
}

function overlapping_shift(shift, shifts) {
    for (var i = 0; i < shifts.length; ++i) {
        if (shift.start_time >= shifts[i].start_time
            && shift.start_time < shifts[i].end_time) {
            return true;
        }
        if (shift.end_time >= shifts[i].start_time
            && shift.end_time < shifts[i].end_time) {
            return true;
        }
    }
    return false;
}

function get_shifts_on_day(shifts, date) {
    var day_of_week = (date.getDay() + 6) % 7;
    var shifts_on_day = shifts.filter(s => s.day_of_week == day_of_week);
    var found_shifts = [];

    // start with latest created get first non-overlapping shifts
    shifts_on_day.sort((s1, s2) => s1.id > s2.id ? -1 : 1)
    for (var i = 0; i < shifts_on_day.length; ++i) {
        var shift = shifts_on_day[i];

        if (!overlapping_shift(shift, found_shifts)) {
            found_shifts.push(shift);
        }
    }
    return found_shifts.sort((s1,s2) => s1.start_time < s2.start_time ? -1 : 1);
}

function get_shifts(shifts, date, days) {
    var found_shifts = [];

    while (days > 0) {
        var date = new Date(date.valueOf());
        var shifts_on_day = get_shifts_on_day(shifts, date);
        var entry = {'date': date, 'shifts_on_date': shifts_on_day};
        found_shifts.push(entry);
        days -= 1;
        date.setDate(date.getDate() + 1);
    };
    return found_shifts;
}

function minutes_to_time_string(m) {
    var hours = Math.floor(m/60);
    var minutes = m - hours * 60;
    var ampm = hours < 12 ? "AM" : "PM";

    if (hours > 12) {
        hours -= 12;
    } else if (hours == 0) {
        hours = 12;
    }
    return hours.toString(10) + ":" + (minutes < 10 ? "0": "") + minutes.toString(10) + " " + ampm;
}

/*
    If the shift list is empty, there are no shifts.
    If the shift list doesn't have any shifts with roles, there are no shifts.
*/
function any_shifts(shift_list) {
    for (var shift_index = 0; shift_index < shift_list.length; ++shift_index) {
        if (shift_list[shift_index].roles.length > 0) {
            return true;
        }
    }
    return false;
}

function update_shift_editor(employees, shifts, div_id) {
    var container = document.getElementById(div_id);
    var start_date = new Date();

    start_date.setDate(start_date.getDate() + 1);
    var two_weeks_shifts = get_shifts(shifts, start_date, 14);
    var display_text = "";
    for (var day_index = 0; day_index < two_weeks_shifts.length; ++day_index) {
        var day_shifts = two_weeks_shifts[day_index];
        if (any_shifts(day_shifts.shifts_on_date)) {
            display_text += "Date: " + day_shifts.date + "\n<ul>\n";
            for (var shift_index = 0; shift_index < day_shifts.shifts_on_date.length; ++shift_index) {
                var shift = day_shifts.shifts_on_date[shift_index];
                if (shift.roles.length) {
                    display_text += "<li>" + minutes_to_time_string(shift.start_time)
                                           + " - "
                                           + minutes_to_time_string(shift.end_time)
                                           + "\n<ul>\n";

                    for (var role_index = 0; role_index < shift.roles.length; ++role_index) {
                        role = shift.roles[role_index];
                        display_text += "<li>" + role.number.toString(10) + " x " + role.role + "</li>\n";
                    }
                    display_text += "</ul>\n</li>\n";
                }
            }
            display_text += "</ul>";
        }
    }
    container.innerHTML = display_text;
}
