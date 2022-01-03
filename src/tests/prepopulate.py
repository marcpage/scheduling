import model

USERS = [
    {'name': "Admin", "email": "admin@restaurant.com", "password": "admin", "admin": True, "hours_limit": 0.0},
    {'name': "Brianna", "email": "brianna@restaurant.com", "password": "brianna", "admin": False, "hours_limit": 0.0},
    {'name': "Kenneth", "email": "kenneth@restaurant.com", "password": "kenneth", "admin": False, "hours_limit": 0.0},
    {'name': "Michael", "email": "michael@restaurant.com", "password": "michael", "admin": False, "hours_limit": 0.0},
]

RESTAURANTS = [
    {'name': "Baris Pasta & Pizza", "gm": "brianna@restaurant.com"},
    {'name': "Taco Bell", "gm": "michael@restaurant.com"},
]

ROLES = [
    'Dishwasher', 'Busser', 'Server', 'Phones', 'Phones', 'Cashier', 'Prep', 'Open', 'Close', 'Manager', 'Alcohol (18)'
]

def load(storage_url):
    database = model.Database(storage_url)

    for user in USERS:
        database.create_user(**user)

    for restaurant in RESTAURANTS:
        restaurants = database.get_restaurants()
        already_exists = any([True for r in restaurants if r.name.lower() == restaurant['name'].lower()])

        if not already_exists:
            restaurant_entry = database.create_restaurant(restaurant['name'])
            restaurant_entry.gm_id = database.find_user(restaurant['gm']).id

            for role in ROLES:
                database.create_role(restaurant_entry.id, role)

            for user_info in USERS:
                user = database.find_user(user_info['email'])
                if restaurant_entry.gm_id != user.id:
                    database.add_user_to_restaurant(user, restaurant_entry)


    database.close()


