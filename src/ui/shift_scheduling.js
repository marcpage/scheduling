
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

function update_shift_editor(employees, shifts, div_id) {
    var container = document.getElementById(div_id);
    container.innerText = "Shift Editor Here";
}
