#!/usr/bin/env python3

""" scheduling restaurant staff
"""

import argparse
import datetime
import hashlib
import os
from flask import Flask, render_template, request, redirect
import sqlalchemy
import sqlalchemy.ext.declarative

STORAGE_PATH = os.path.join(
    os.environ["HOME"], "Library", "Preferences", "scheduling.sqlite3"
)
STORAGE = "sqlite:///" + STORAGE_PATH


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


class User(Alchemy_Base):
    """user in database"""

    __tablename__ = "user"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    email = sqlalchemy.Column(sqlalchemy.String(50))
    password_hash = sqlalchemy.Column(sqlalchemy.String(64))
    # m = shift manager, a = admin, g = general manager, s = shift worker
    roles = sqlalchemy.Column(sqlalchemy.String(4))
    # last_login = sqlalchemy.Column(sqlalchemy.DateTime)
    # rank = sqlalchemy.Column(sqlalchemy.Float)

    @staticmethod
    def __hash(text):
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
        self.__engine = sqlalchemy.create_engine(self.__db_url)
        factory = sqlalchemy.orm.sessionmaker(bind=self.__engine)
        session = sqlalchemy.orm.scoped_session(factory)
        self.__session = session()
        Alchemy_Base.metadata.create_all(self.__engine)

    def __enter__(self):
        """for with lifetime statements"""
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """close on end of with lifetime"""
        print(exception_type, exception_value, exception_traceback)
        self.close()

    def flush(self):
        """flush all changes to the database"""
        self.__session.commit()

    def close(self):
        """close down the connection to the database"""
        self.flush()
        self.__session.close()


def create_app(storage_url, source_dir, template_dir):
    """create the flask app"""
    app = Flask(__name__, static_folder=source_dir, template_folder=template_dir)
    database = Database(storage_url)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form["email"]
        password = request.form["password"]
        print([email, password])
        return redirect("/welcome")

    @app.route("/welcome")
    def welcome():
        database.flush()
        return render_template("welcome.html")

    @app.errorhandler(404)
    def page_not_found(error):
        print(error)
        return (render_template("404.html", path="???"), 404)

    return app


def parse_args():
    """Parses and returns command line arguments."""

    parser = argparse.ArgumentParser(description="Schedule maker.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="The port to listen on (default 8000)",
    )
    parser.add_argument(
        "-s", "--storage", default=STORAGE, help="SqlAlchemy url to store information"
    )
    parser.add_argument(
        "-u",
        "--ui",
        type=str,
        default="ui",
        help="Path to the directory with ui files.",
    )
    parser.add_argument("-d", "--debug", default=True, help="Run debug server.")
    args = parser.parse_args()

    return args


def main():
    """Entry point. Loop forever unless we are told not to."""

    args = parse_args()
    app = create_app(args.storage, args.ui, os.path.join(args.ui, "template"))
    app.run(host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
