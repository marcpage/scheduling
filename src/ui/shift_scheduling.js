
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

function parseDate (dateString) {
    const parts = dateString.match(/(\d+)/g);
    return new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
}

function daysBetweenDates (d1, d2) {
    return Math.round(Math.abs(d2.getTime() - d1.getTime()) / (1000 * 60 * 60 * 24));
}

function shiftRange (shift) {
    return daysBetweenDates(parseDate(shift.start_date), parseDate(shift.end_date));
}

function overlappingShift (shift, shifts) {
    for (let i = 0; i < shifts.length; ++i) {
        if (shift.start_time >= shifts[i].start_time && shift.start_time < shifts[i].end_time) {
            return true;
        }
        if (shift.end_time >= shifts[i].start_time && shift.end_time < shifts[i].end_time) {
            return true;
        }
    }
    return false;
}

function getShiftsOnDay (shifts, date) {
    const dayOfWeek = (date.getDay() + 6) % 7;
    const shiftsOnDay = shifts.filter(s => s.day_of_week === dayOfWeek);
    const foundShifts = [];

    // start with latest created get first non-overlapping shifts
    shiftsOnDay.sort((s1, s2) => s1.id > s2.id ? -1 : 1)
    for (let i = 0; i < shiftsOnDay.length; ++i) {
        const shift = shiftsOnDay[i];

        if (!overlappingShift(shift, foundShifts)) {
            foundShifts.push(shift);
        }
    }
    return foundShifts.sort((s1, s2) => s1.start_time < s2.start_time ? -1 : 1);
}

function getShifts (shifts, date, days) {
    const foundShifts = [];

    while (days > 0) {
        date = new Date(date.valueOf());
        const shiftsOnDay = getShiftsOnDay(shifts, date);
        const entry = { date: date, shifts_on_date: shiftsOnDay };
        foundShifts.push(entry);
        days -= 1;
        date.setDate(date.getDate() + 1);
    };
    return foundShifts;
}

function minutesToTimeString (m) {
    let hours = Math.floor(m / 60);
    const minutes = m - hours * 60;
    const ampm = hours < 12 ? 'AM' : 'PM';

    if (hours > 12) {
        hours -= 12;
    } else if (hours === 0) {
        hours = 12;
    }
    return hours.toString(10) + ':' + (minutes < 10 ? '0' : '') + minutes.toString(10) + ' ' + ampm;
}

/*
    If the shift list is empty, there are no shifts.
    If the shift list doesn't have any shifts with roles, there are no shifts.
*/
function anyShifts (shiftList) {
    for (let shiftIndex = 0; shiftIndex < shiftList.length; ++shiftIndex) {
        if (shiftList[shiftIndex].roles.length > 0) {
            return true;
        }
    }
    return false;
}

function updateShiftEditor (employees, shifts, divId) {
    const container = document.getElementById(divId);
    const startDate = new Date();

    startDate.setDate(startDate.getDate() + 1);
    const twoWeeksShifts = getShifts(shifts, startDate, 14);
    let displayText = '';
    for (let dayIndex = 0; dayIndex < twoWeeksShifts.length; ++dayIndex) {
        const dayShifts = twoWeeksShifts[dayIndex];
        if (anyShifts(dayShifts.shifts_on_date)) {
            displayText += 'Date: ' + dayShifts.date + '\n<ul>\n';
            for (let shiftIndex = 0; shiftIndex < dayShifts.shifts_on_date.length; ++shiftIndex) {
                const shift = dayShifts.shifts_on_date[shiftIndex];
                if (shift.roles.length) {
                    displayText += '<li>' + minutesToTimeString(shift.start_time) +
                                           ' - ' +
                                           minutesToTimeString(shift.end_time) +
                                           '\n<ul>\n';

                    for (let roleIndex = 0; roleIndex < shift.roles.length; ++roleIndex) {
                        const role = shift.roles[roleIndex];
                        displayText += '<li>' + role.number.toString(10) + ' x ' + role.role + '</li>\n';
                    }
                    displayText += '</ul>\n</li>\n';
                }
            }
            displayText += '</ul>';
        }
    }
    container.innerHTML = displayText;
}
