
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

/*
    Get a list of non-overlapping shifts for the date.
    TODO: This does not work right now
*/
function get_shifts_on_day(shifts, date) {
    var day_of_week = (date.getDay() + 6) % 7;
    var shifts_on_day = shifts.filter(s => s.day_of_week == day_of_week);

    shifts_on_day.sort((e1, e2) => e1.start_time < e2.start_time ? -1 : (e1.start_time > e2.start_time ? 1 : 0));
    var best_shift = undefined;
    for (var i = 0; i < shifts_on_day.length; ++i) {
        var evaluate = shifts_on_day[i];

        if (!best_shift || shift_range(evaluate) < shift_range(best_shift)) {
            best_shift = evaluate;
        }
    }
    return shifts;
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

function update_shift_editor(employees, shifts, div_id) {
    var container = document.getElementById(div_id);
    var start_date = new Date();

    start_date.setDate(start_date.getDate() + 1);
    container.innerText = get_shifts(shifts, start_date, 14);
}
