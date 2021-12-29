#!/usr/bin/env python3

""" The model of the data
"""

import datetime
import hashlib
import threading

import sqlalchemy
import sqlalchemy.ext.declarative


# W0223: Method 'python_type' is abstract in class 'TypeEngine' but is not overridden
class Date(sqlalchemy.types.TypeDecorator):  # pylint: disable=W0223
    """database date format"""

    impl = sqlalchemy.types.Date

    def process_bind_param(self, value, dialect):
        try:  # if it is a string, parse it, otherwise it must be datetime object
            return datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
        except TypeError:
            return value

    def process_result_value(self, value, dialect):
        return value

    def process_literal_param(self, value, dialect):
        return value


Alchemy_Base = sqlalchemy.ext.declarative.declarative_base()


# R0903: Too few public methods (0/2) (too-few-public-methods)
class RoleValue(Alchemy_Base):  # pylint: disable=R0903
    """the value of a user for the role for the gm"""

    __tablename__ = "role_value"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    gm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    gm = sqlalchemy.orm.relationship("User", foreign_keys=[gm_id])
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User", foreign_keys=[user_id])
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    priority = sqlalchemy.Column(sqlalchemy.Float)

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} gm = "{self.gm.name}" user = "{self.user.name}" '
            + f"role = {self.role.name} priority = {self.priority}"
        )


default_shift_roles = sqlalchemy.Table(
    "default_shift_roles",
    Alchemy_Base.metadata,
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey("role.id")),
    sqlalchemy.Column("default_shift_id", sqlalchemy.ForeignKey("default_shift.id")),
)


# R0903: Too few public methods (0/2) (too-few-public-methods)
class DefaultShift(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "default_shift"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    day_of_week = sqlalchemy.Column(sqlalchemy.String(10))
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    roles = sqlalchemy.orm.relationship("Role", secondary=default_shift_roles)

    def __repr__(self):
        """display string"""
        roles = ", ".join([r.name for r in self.roles])
        return (
            f'id = {self.id} day = "{self.day_of_week}" start time = "{self.start_time}" '
            + f"end time = {self.end_time} priority = {self.priority} "
            + f"start date = {self.start_date} end date = {self.end_date} "
            + f'roles = "{roles}"'
        )


shift_roles = sqlalchemy.Table(
    "shift_roles",
    Alchemy_Base.metadata,
    sqlalchemy.Column("role_id", sqlalchemy.ForeignKey("role.id")),
    sqlalchemy.Column("shift_id", sqlalchemy.ForeignKey("shift.id")),
)


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Shift(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "shift"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    note = sqlalchemy.Column(sqlalchemy.String(50))
    roles = sqlalchemy.orm.relationship("Role", secondary=shift_roles)

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} date = "{self.date}" start time = "{self.start_time}" '
            + f'end time = {self.end_time} priority = {self.priority} note="{self.note}"'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserRolePreference(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "user_role_preference"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    priority = sqlalchemy.Column(sqlalchemy.Float)

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} user = "{self.user.name}" role = "{self.role.name}" '
            + f"priority = {self.priority}"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserLimits(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "user_limits"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    gm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    gm = sqlalchemy.orm.relationship("User", foreign_keys=[gm_id])
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User", foreign_keys=[user_id])
    hours_limit = sqlalchemy.Column(sqlalchemy.Integer)
    notes = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} gm = "{self.gm.name}" user = "{self.user.name}" '
            + f"hours = {self.hours_limit} notes = {self.notes}"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class ScheduledShift(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "scheduled_shift"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    shift_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shift.id"))
    shift = sqlalchemy.orm.relationship("Shift")
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("role.id"))
    role = sqlalchemy.orm.relationship("Role")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    draft = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} date = "{self.date}" shift = "{self.shift}" role = {self.role.name}'
            + f"user = {self.user.name} draft = {self.draft}"
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserShiftDefaultRequest(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "user_shift_default_request"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    day_of_week = sqlalchemy.Column(sqlalchemy.String(10))
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    note = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} user="{self.user.name}" restaurant="{self.restaurant.name}" '
            + f"day = {self.day_of_week} start_time = {self.start_time} end_time = {self.end_time} "
            + f'priority = {self.priority} note = "{self.note}"'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class UserShfitRequest(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "user_shift_request"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = sqlalchemy.orm.relationship("User")
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    start_time = sqlalchemy.Column(sqlalchemy.Integer)
    end_time = sqlalchemy.Column(sqlalchemy.Integer)
    priority = sqlalchemy.Column(sqlalchemy.Float)
    note = sqlalchemy.Column(sqlalchemy.String(50))

    def __repr__(self):
        """display string"""
        return (
            f'id = {self.id} user="{self.user.name}" restaurant="{self.restaurant.name}" '
            + f"date = {self.date} start_time = {self.start_time} end_time = {self.end_time} "
            + f'priority = {self.priority} note = "{self.note}"'
        )


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Role(Alchemy_Base):  # pylint: disable=R0903
    """doc string"""

    __tablename__ = "role"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    restaurant_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("restaurant.id")
    )
    restaurant = sqlalchemy.orm.relationship("Restaurant")


# R0903: Too few public methods (0/2) (too-few-public-methods)
class Restaurant(Alchemy_Base):  # pylint: disable=R0903
    """location"""

    __tablename__ = "restaurant"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    gm_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    gm = sqlalchemy.orm.relationship("User")

    def __repr__(self):
        """display string"""
        return f'id = {self.id} name="{self.name}" gm="{self.gm.name}"'


# R0903: Too few public methods (0/2) (too-few-public-methods)
class User(Alchemy_Base):  # pylint: disable=R0903
    """user in database"""

    __tablename__ = "user"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    email = sqlalchemy.Column(sqlalchemy.String(50))
    password_hash = sqlalchemy.Column(sqlalchemy.String(64))
    hours_limit = sqlalchemy.Column(sqlalchemy.Integer)
    admin = sqlalchemy.Column(sqlalchemy.Boolean)
    # m = schedule manager, a = admin, g = general manager, s = shift worker
    # roles = sqlalchemy.Column(sqlalchemy.String(4))
    # last_login = sqlalchemy.Column(sqlalchemy.DateTime)
    # rank = sqlalchemy.Column(sqlalchemy.Float)

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
        return User.__hash(password) == self.password_hash

    def __repr__(self):
        """display string"""
        return f'id = {self.id} name="{self.name}" email="{self.email}"'


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
                self.__sessions[thread_id] = self.__session_creator()

        return self.__sessions[thread_id]

    def __add(self, entry):
        self.__session().add(entry)
        self.__session().commit()
        return entry

    def flush(self):
        """flush all changes to the database"""
        self.__session().commit()

    def close(self):
        """close down the connection to the database"""
        self.__session().commit()
        self.__session().close()

    def create_user(self, email, password, name, **kwargs):
        """doc string"""
        return self.__add(
            User(
                email=email,
                password_hash=User.hash_password(password),
                name=name,
                **kwargs,
            )
        )

    def get_user(self, user_id):
        """doc string"""
        return self.__session().query(User).filter(User.id == user_id).one_or_none()

    def find_user(self, email):
        """doc string"""
        return (
            self.__session()
            .query(User)
            .filter(sqlalchemy.func.lower(User.email) == sqlalchemy.func.lower(email))
            .one_or_none()
        )

    def get_users(self):
        return self.__session().query(User).all()

    def create_restaurant(self, name):
        """doc string"""
        return self.__add(Restaurant(name=name))

    def get_restaurant(self, restaurant_id):
        """doc string"""
        return (
            self.__session()
            .query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .one_or_none()
        )

    def get_restaurants(self):
        return self.__session().query(Restaurant).all()
