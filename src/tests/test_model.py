#!/user/bin/env python3

""" Testing data model
"""

import model
import unittest
import sys
import os


class TestUser(unittest.TestCase):
    storage_path = os.path.join("bin", "tests", "scheduling_%s.sqlite3")
    storage_url = "sqlite:///" + storage_path

    def setUp(self):
        if not os.path.isdir(os.path.split(self.storage_path)[0]):
            os.makedirs(os.path.split(self.storage_path)[0])

    def test_create(self):
        database = model.Database(self.storage_url % (sys._getframe().f_code.co_name))
        u1 = database.create_user(
            "u@c.com", "password", "Joe", hours_limit=40.0, admin=False
        )
        u2 = database.find_user("u@c.com")
        self.assertEqual(u1.id, u2.id)

    def test_create_email_once(self):
        database = model.Database(self.storage_url % (sys._getframe().f_code.co_name))
        u1 = database.create_user(
            "u@c.com", "password", "Joe", hours_limit=40.0, admin=False
        )
        u2 = database.create_user(
            "U@c.com", "setec", "John", hours_limit=20.0, admin=True
        )
        self.assertEqual(u1.id, u2.id)

    def test_get_user(self):
        database = model.Database(self.storage_url % (sys._getframe().f_code.co_name))
        u1 = database.create_user(
            "a@c.com", "password", "A", hours_limit=10.0, admin=False
        )
        u2 = database.create_user(
            "b@c.com", "setec", "B", hours_limit=20.0, admin=False
        )
        u3 = database.create_user(
            "c@c.com", "astronomy", "C", hours_limit=30.0, admin=False
        )
        u4 = database.create_user(
            "D@c.com", "too many secrets", "D", hours_limit=40.0, admin=False
        )
        a1 = database.get_user(u1.id)
        a2 = database.get_user(u2.id)
        a3 = database.get_user(u3.id)
        a4 = database.get_user(u4.id)
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)
        self.assertIsNotNone(a3)
        self.assertIsNotNone(a4)
        self.assertEqual(u1.name, a1.name)
        self.assertEqual(u1.name, "A")
        self.assertEqual(u1.password_hash, a1.password_hash)
        self.assertEqual(u1.email, a1.email)
        self.assertEqual(u1.email, "a@c.com")
        self.assertEqual(u2.name, a2.name)
        self.assertEqual(u2.name, "B")
        self.assertEqual(u2.password_hash, a2.password_hash)
        self.assertEqual(u2.email, a2.email)
        self.assertEqual(u2.email, "b@c.com")
        self.assertEqual(u2.name, a2.name)
        self.assertEqual(u3.name, "C")
        self.assertEqual(u3.password_hash, a3.password_hash)
        self.assertEqual(u3.email, a3.email)
        self.assertEqual(u3.email, "c@c.com")
        self.assertEqual(u3.name, a3.name)
        self.assertEqual(u4.name, "D")
        self.assertEqual(u4.password_hash, a4.password_hash)
        self.assertEqual(u4.email, a4.email)
        self.assertEqual(u4.email, "D@c.com")

    def test_list_users(self):
        database = model.Database(self.storage_url % (sys._getframe().f_code.co_name))
        u1 = database.create_user(
            "a@c.com", "password", "A", hours_limit=10.0, admin=False
        )
        u2 = database.create_user(
            "b@c.com", "setec", "B", hours_limit=20.0, admin=False
        )
        u3 = database.create_user(
            "c@c.com", "astronomy", "C", hours_limit=30.0, admin=False
        )
        u4 = database.create_user(
            "D@c.com", "too many secrets", "D", hours_limit=40.0, admin=False
        )
        users = database.get_users()
        user_ids = [u.id for u in users]
        user_names = [u.name for u in users]
        user_emails = [u.email for u in users]
        user_passwords = [u.password_hash for u in users]
        self.assertTrue(u1.id in user_ids)
        self.assertTrue(u2.id in user_ids)
        self.assertTrue(u3.id in user_ids)
        self.assertTrue(u4.id in user_ids)
        self.assertTrue(u1.name in user_names)
        self.assertTrue(u2.name in user_names)
        self.assertTrue(u3.name in user_names)
        self.assertTrue(u4.name in user_names)
        self.assertTrue(u1.email in user_emails)
        self.assertTrue(u2.email in user_emails)
        self.assertTrue(u3.email in user_emails)
        self.assertTrue(u4.email in user_emails)
        self.assertTrue(u1.password_hash in user_passwords)
        self.assertTrue(u2.password_hash in user_passwords)
        self.assertTrue(u3.password_hash in user_passwords)
        self.assertTrue(u4.password_hash in user_passwords)


if __name__ == "__main__":
    unittest.main()
