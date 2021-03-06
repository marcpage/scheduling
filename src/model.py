#!/usr/bin/env python3

""" The model of the data
"""

import datetime
import hashlib
import threading
import time

import sqlalchemy
import sqlalchemy.ext.declarative


# W0223: Method 'python_type' is abstract in class 'TypeEngine' but is not overridden
class Date(sqlalchemy.types.TypeDecorator):  # pylint: disable=W0223
    """database date format"""

    impl = sqlalchemy.types.Date

    def process_bind_param(self, value, dialect):
        # if it is a string, parse it, otherwise it must be datetime object
        try:
            return datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
        except TypeError:
            return value

    def process_result_value(self, value, dialect):
        return value

    def process_literal_param(self, value, dialect):
        return value


Alchemy_Base = sqlalchemy.ext.declarative.declarative_base()


# R0903: Too few public methods (0/2) (too-few-public-methods)
class ShiftRole(Alchemy_Base):  # pylint: disable=R0903
    """How many people of a given role are needed for a given shift.
    role_id / role - The role for the shift
    shift_id / shift - The shift
    number - the number of people of this role needed for this shift
    """

    __tablename__ = "shift_roles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    shift_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shift.id"))
    shift = sqlalchemy.orm.relationship("Shift")
    number = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        """display string"""
        return (
            f"Shift(id={self.id} "
            + f'role="{self.role}" '
            + f'shift="{self.shift}" '
            + f'number="{self.number}")'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Shift(Alchemy_Base):  # pylint: disable=R0903
    """Shifts to be scheduled during a date range
    restaurant_id / restaurant - The restaurant for this shift
    day_of_week - The day of the week 0 = Monday
    start_time - The number of minutes since midnight that the shift starts
    end_time - The number of minutes since midnight that the shift ends
    priority - The priority to fill this shift
    start_date - The date this default is first available
    end_date - The last date this default is viable
    roles - The roles needed for the shift
    """

    __tablename__ = "shift"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    day_of_week = sqlalchemy.Column(sqlalchemy.Integer)
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    roles = sqlalchemy.orm.relationship("ShiftRole", viewonly=True)

    def __repr__(self):
        """display string"""
        roles = ", ".join([f"{r.role.name} x {r.number}" for r in self.roles])
        return (
            f"Shift(id={self.id} "
            + f'day="{self.day_of_week}" '
            + f'start time="{self.start_time}" '
            + f"end time={self.end_time} "
            + f"priority={self.priority} "
            + f"start date={self.start_date} "
            + f"end date={self.end_date} "
            + f"roles={roles} "
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserRolePreference(Alchemy_Base):  # pylint: disable=R0903
    """The priority of a role at a restaurant for an employee and GM's priority
    user_id / user - The employee
    role_id / role - The role at a given restaurant
    priority - The employee's priority for this restaurant's role
    gm_priority - The GM's priority for this employee for this role
    """

    __tablename__ = "user_role_preference"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    priority = sqlalchemy.Column(sqlalchemy.Float)
    gm_priority = sqlalchemy.Column(sqlalchemy.Float)

    def __repr__(self):
        """display string"""
        return (
            f'UserRolePreference(id={self.id} user="{self.user.name}" '
            f'role="{self.role.name}" @ "{self.role.restaurant.name}" '
            + f"priority={self.priority})"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserLimits(Alchemy_Base):  # pylint: disable=R0903
    """The GM's notes and hours limit for an employee
    restaurant_id - The restaurant for these limits
    user_id / user - The employee
    hours_limit - The maximum number of hours to schedule an employee
    notes - GM's notes about the employee
    """

    __tablename__ = "user_limits"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    hours_limit = sqlalchemy.Column(sqlalchemy.Integer)
    notes = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f"UserLimits(id={self.id} "
            + f'gm="{self.gm.name}" '
            + f'user="{self.user.name}" '
            + f"hours={self.hours_limit} "
            + f"notes={self.notes})"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class ScheduledShift(Alchemy_Base):  # pylint: disable=R0903
    """An instance of a scheduled shift
    date - The date of the shift
    shift_id / shift - The shift that is scheduled
    role_id / role - The role for this shift
    user_id / user - The employee scheduled
    draft - If not draft then it is published for employee to see
    notes - Notes to the employee
    """

    __tablename__ = "scheduled_shift"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    shift_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shift.id"))
    shift = sqlalchemy.orm.relationship("Shift")
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    draft = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    notes = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f"ScheduledShift(id={self.id} "
            + f'date="{self.date}" '
            + f'shift="{self.shift}" '
            + f"role={self.role.name} "
            + f"user={self.user.name} "
            + f"draft={self.draft})"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserAvailability(Alchemy_Base):  # pylint: disable=R0903
    """The times available for an employee
    user_id / user - The employee
    restaurant_id / restaurant - The restaurant
    day_of_week - The day of the week 0 = Monday
    start_time - The number of minutes since midnight that the priority starts
    end_time - The number of minutes since midnight that the priority ends
    start_date - The date this default is first available
    end_date - The last date this default is viable
    priority - Meaning of this time slot
        1 - want to work
        2 - could work
        3 - prefer not to work
        4 - cannot work
    note - Any notes about this time slot
    """

    __tablename__ = "user_availability"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    day_of_week = sqlalchemy.Column(sqlalchemy.Integer)
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    note = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f'UserAvailability(id={self.id} user="{self.user.name}" '
            + f'restaurant="{self.restaurant.name}" day={self.day_of_week} '
            + f"start_time={self.start_time} end_time={self.end_time} "
            + f'priority={self.priority} note="{self.note}")'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Role(Alchemy_Base):  # pylint: disable=R0903
    """The employee roles at a restaurant
    name - The name of the role
    restaurant_id / restaurant - the restaurant this role is for
    preferences - all the employee preferences for this role
    """

    __tablename__ = "role"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    preferences = sqlalchemy.orm.relationship("UserRolePreference", viewonly=True)

    def __repr__(self):
        """display string"""
        return (
            f'Role(id={self.id} name="{self.name}" '
            f'restaurant="{self.restaurant.name}")'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Restaurant(Alchemy_Base):  # pylint: disable=R0903
    """The restaurant location
    name - the name of the restaurant
    gm_id / gm - the general manager (may be null)
    roles - list of Roles associated with the restaurant
    """

    __tablename__ = "restaurant"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    gm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    gm = sqlalchemy.orm.relationship("User")
    roles = sqlalchemy.orm.relationship("Role", viewonly=True)
    shifts = sqlalchemy.orm.relationship("Shift", viewonly=True)

    def __repr__(self):
        """display string"""
        return (
            f'Restaurant(id={self.id} name="{self.name}" '
            + f'gm="{self.gm.name if self.gm else None}")'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class User(Alchemy_Base):  # pylint: disable=R0903
    """Represents an employee
    name - Full employee name
    email - The email to contact the employee at
    password_hash - sha256 hash of the user's password
    hours_limit - The maximum number of hours per week
    admin - true if this is an admin account
    gm_at - list of restaurants this user is a gm at
    roles - the role priorities at each restaurant
    """

    __tablename__ = "user"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    email = sqlalchemy.Column(sqlalchemy.String(50))
    password_hash = sqlalchemy.Column(sqlalchemy.String(64))
    hours_limit = sqlalchemy.Column(sqlalchemy.Integer)
    admin = sqlalchemy.Column(sqlalchemy.Boolean)
    gm_at = sqlalchemy.orm.relationship("Restaurant", viewonly=True)
    roles = sqlalchemy.orm.relationship("UserRolePreference", viewonly=True)
    availabilities = sqlalchemy.orm.relationship("UserAvailability", viewonly=True)

    @staticmethod
    def hash_password(text):
        """hash some random text"""
        hasher = hashlib.new("sha256")
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()

    def set_password(self, password):
        """Set the user password hash"""
        self.password_hash = User.__hash(password)

    def password_matches(self, password):
        """does this match the password"""
        return User.hash_password(password) == self.password_hash

    def __repr__(self):
        """display string"""
        return f'User(id={self.id} name="{self.name}" email="{self.email}")'


class Database:
    """stored information"""

    def __init__(self, db_url):
        """create db"""
        self.__db_url = db_url
        self.__sessions = {}
        self.__session_lock = threading.Lock()
        engine = sqlalchemy.create_engine(self.__db_url)
        self.__factory = sqlalchemy.orm.sessionmaker(bind=engine)
        Alchemy_Base.metadata.create_all(engine)
        self.__session_creator = sqlalchemy.orm.scoped_session(self.__factory)

    def __session(self):
        thread_id = threading.current_thread().ident

        with self.__session_lock:
            if thread_id not in self.__sessions:
                self.__sessions[thread_id] = {
                    "session": self.__session_creator(),
                    "access": time.time(),
                }
            else:
                self.__sessions[thread_id]["access"] = time.time()
        return self.__sessions[thread_id]["session"]

    def __add(self, entry):
        self.__session().add(entry)
        self.__session().commit()
        return entry

    def sessions(self):
        """Return the number of active sessions"""
        now = time.time()
        with self.__session_lock:
            return [now - s["access"] for s in self.__sessions.values()]

    def flush(self):
        """flush all changes to the database"""
        self.__session().commit()

    def close(self):
        """close down the connection to the database"""
        self.__session().commit()
        self.__session().close()

    # Mark: User API

    def create_user(self, email, password, name, **kwargs):
        """create a new employee entry"""
        found = self.find_user(email)
        return (
            self.__add(
                User(
                    email=email,
                    password_hash=User.hash_password(password),
                    name=name,
                    **kwargs,
                )
            )
            if found is None
            else found
        )

    def get_user(self, user_id):
        """Get a user by its id"""
        return (
            self.__session().query(User).filter(User.id == int(user_id)).one_or_none()
            if user_id is not None
            else None
        )

    def add_user_to_restaurant(self, user, restaurant):
        """Makes sure the employee has a UserRolePreference for
        every restaurant role"""
        priority = 1.0 + (max([r.priority for r in user.roles]) if user.roles else 0.0)
        preferred_roles = [r.id for r in user.roles]

        for role in restaurant.roles:
            if role.id not in preferred_roles:
                self.__add(
                    UserRolePreference(
                        user_id=user.id,
                        role_id=role.id,
                        priority=priority,
                        gm_priority=priority,
                    )
                )
                priority += 1.0

    def find_user(self, email):
        """Get a user by email (case insensitive)"""
        return (
            self.__session()
            .query(User)
            .filter(sqlalchemy.func.lower(User.email) == sqlalchemy.func.lower(email))
            .one_or_none()
        )

    def get_users(self):
        """Get list of all users"""
        return self.__session().query(User).all()

    # Mark: Availability API

    def create_availability(self, user, restaurant, day_of_week, **kwargs):
        """Create an availability"""
        return self.__add(
            UserAvailability(
                user_id=user.id,
                restaurant_id=restaurant.id,
                day_of_week=day_of_week,
                start_time=kwargs["start_time"],
                start_date=kwargs["start_date"],
                end_date=kwargs["end_date"],
                end_time=kwargs["end_time"],
                priority=kwargs["priority"],
                note=kwargs["note"],
            )
        )

    # Mark: Restaurant API

    def create_restaurant(self, name):
        """Create a new restaurant"""
        return self.__add(Restaurant(name=name))

    def get_restaurant(self, restaurant_id):
        """Get a restaurant by id"""
        return (
            (
                self.__session()
                .query(Restaurant)
                .filter(Restaurant.id == restaurant_id)
                .one_or_none()
            )
            if restaurant_id is not None
            else None
        )

    def get_restaurants(self):
        """Get list of all restaurants"""
        return self.__session().query(Restaurant).all()

    def create_role(self, restaurant_id, name):
        """Create a new role for a restaurant"""
        return (
            self.__add(Role(name=name, restaurant_id=restaurant_id))
            if len(name) > 0
            else None
        )

    def create_shift(self, restaurant, day_of_week, **kwargs):
        """Create a new shift"""
        return self.__add(
            Shift(
                restaurant_id=restaurant.id,
                day_of_week=day_of_week,
                start_time=kwargs["start_time"],
                end_time=kwargs["end_time"],
                start_date=kwargs["start_date"],
                end_date=kwargs["end_date"],
                priority=kwargs["priority"],
            )
        )

    def add_role_to_shift(self, shift, role, number=1):
        """Add roles to a shift"""
        shift_role = (
            self.__session()
            .query(ShiftRole)
            .filter(
                sqlalchemy.and_(
                    ShiftRole.shift_id == shift.id, ShiftRole.role_id == role.id
                )
            )
            .one_or_none()
        )
        if shift_role is not None:
            shift_role.number += number
        else:
            shift_role = self.__add(
                ShiftRole(role_id=role.id, shift_id=shift.id, number=number)
            )
        return shift_role
