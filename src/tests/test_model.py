#!/user/bin/env python3

""" Testing data model
"""

# TODO: Test add_user_to_restaurant
# TODO: More find_user tests
# TODO: Test create_role

import model
import unittest
import sys
import os

STORAGE_PATH = os.path.join("bin", "tests", "scheduling_%s.sqlite3")
STORAGE_URL = f"sqlite:///{STORAGE_PATH}"

USERS = [
    {
        "email": "u@c.com",
        "password": "password",
        "name": "Joe",
        "hours_limit": 40.0,
        "admin": False,
    },
    {
        "email": "a@c.com",
        "password": "setec",
        "name": "John",
        "hours_limit": 10.0,
        "admin": False,
    },
    {
        "email": "b@c.com",
        "password": "astronomy",
        "name": "John",
        "hours_limit": 20.0,
        "admin": False,
    },
    {
        "email": "c@c.com",
        "password": "too many secrets",
        "name": "John",
        "hours_limit": 30.0,
        "admin": False,
    },
    {
        "email": "d@c.com",
        "password": "let me in",
        "name": "John",
        "hours_limit": 40.0,
        "admin": False,
    },
]
RESTAURANTS = [
    "Baris Pasta & Pizza",
    "Taco Bell",
    "Fogonero Venezuelan",
    "Iron Fish Sushi & Grill",
    "Rec's Hushpuppie Heaven",
    "Pecan Street Station",
    "El Rincon Mexican Restaurant",
    "La Casita",
    "Huahuasco Grill Mexican Cuisine",
    "Stuff'em",
    "Krab Kingz",
    "Pflugerville Taco House",
    "Island Fork - Jamaican/Caribbean Cuisine",
    "Springhill Restaurant",
    "Pita Shack - Best Halal Food In Pflugerville",
    "Red Rooster's Pub & Grub",
]
if not os.path.isdir(os.path.split(STORAGE_PATH)[0]):
    os.makedirs(os.path.split(STORAGE_PATH)[0])


def open_db(test_function_name):
    if os.path.isfile(STORAGE_PATH % (test_function_name)):
        os.unlink(STORAGE_PATH % (test_function_name))
    return model.Database(STORAGE_URL % (test_function_name))


class TestUser(unittest.TestCase):
    def test_create(self):
        database = open_db(sys._getframe().f_code.co_name)
        u1 = database.create_user(**USERS[0])
        u2 = database.find_user(USERS[0]["email"])
        self.assertEqual(u1.id, u2.id)

    def test_create_email_once(self):
        database = open_db(sys._getframe().f_code.co_name)
        u1 = database.create_user(**USERS[0])
        u2 = database.create_user(
            "U@c.com", "setec", "John", hours_limit=20.0, admin=True
        )
        self.assertEqual(u1.id, u2.id)

    def test_get_user(self):
        database = open_db(sys._getframe().f_code.co_name)
        users = [database.create_user(**u) for u in USERS]
        looked_up = [database.get_user(u.id) for u in users]
        for index in range(0, len(looked_up)):
            self.assertIsNotNone(
                looked_up[index], f"expected: {users[index]} got: {looked_up[index]}"
            )
            self.assertEqual(
                looked_up[index].name,
                USERS[index]["name"],
                f"expected: {USERS[index]} got: {looked_up[index]}",
            )
            self.assertEqual(
                looked_up[index].name,
                users[index].name,
                f"expected: {users[index]} got: {looked_up[index]}",
            )
            self.assertEqual(
                looked_up[index].password_hash,
                users[index].password_hash,
                f"expected: {users[index]} got: {looked_up[index]}",
            )
            self.assertEqual(
                looked_up[index].email,
                USERS[index]["email"],
                f"expected: {USERS[index]} got: {looked_up[index]}",
            )
            self.assertEqual(
                looked_up[index].email,
                users[index].email,
                f"expected: {users[index]} got: {looked_up[index]}",
            )

    def test_get_users(self):
        database = open_db(sys._getframe().f_code.co_name)
        created = [database.create_user(**u) for u in USERS]
        users = database.get_users()
        user_ids = [u.id for u in users]
        user_names = [u.name for u in users]
        user_emails = [u.email for u in users]
        user_passwords = [u.password_hash for u in users]
        for index in range(0, len(USERS)):
            self.assertTrue(
                created[index].id in user_ids,
                f"could not find id {created[index]} created as {USERS[index]} in {user_ids}",
            )
            self.assertTrue(
                created[index].name in user_names,
                f"could not find name {created[index]} created as {USERS[index]} in {user_names}",
            )
            self.assertTrue(
                created[index].email in user_emails,
                f"could not find email {created[index]} created as {USERS[index]} in {user_emails}",
            )
            self.assertTrue(
                created[index].password_hash in user_passwords,
                f"could not find password {created[index]} created as {USERS[index]} in {user_passwords}",
            )


class TestRestaurant(unittest.TestCase):
    def test_create_restaurant(self):
        database = open_db(sys._getframe().f_code.co_name)
        r1 = database.create_restaurant(RESTAURANTS[0])
        r2 = database.get_restaurant(r1.id)
        self.assertEqual(r1.id, r2.id)

    def test_get_restaurants(self):
        database = open_db(sys._getframe().f_code.co_name)
        created = [database.create_restaurant(r) for r in RESTAURANTS]
        listed = database.get_restaurants()
        restaurant_ids = [l.id for l in listed]
        restaurant_names = [l.name for l in listed]
        for index in range(0, len(RESTAURANTS)):
            self.assertTrue(
                created[index].id in restaurant_ids,
                f"could not find id {created[index]} created as {RESTAURANTS[index]} in {restaurant_ids}",
            )
            self.assertTrue(
                created[index].name in restaurant_names,
                f"could not find name {created[index]} created as {RESTAURANTS[index]} in {restaurant_names}",
            )
            self.assertTrue(
                RESTAURANTS[index] in restaurant_names,
                f"could not find name {RESTAURANTS[index]} in {restaurant_names}",
            )


if __name__ == "__main__":
    unittest.main()
