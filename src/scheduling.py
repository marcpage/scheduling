#!/usr/bin/env python3

""" scheduling restaurant staff
"""

import argparse
import os
from flask import Flask, render_template, request, redirect, make_response
import model

STORAGE_PATH = os.path.join(
    os.environ["HOME"], "Library", "Preferences", "scheduling.sqlite3"
)
STORAGE = "sqlite:///" + STORAGE_PATH


def create_app(storage_url, source_dir, template_dir):
    """create the flask app"""
    app = Flask(__name__, static_folder=source_dir, template_folder=template_dir)
    database = model.Database(storage_url)

    @app.route("/")
    def home():
        user_id = request.cookies.get("user_id")
        import sys

        sys.stderr.write("user_id = %s\n" % (user_id))
        user = database.get_user(int(user_id)) if user_id is not None else user_id
        return render_template("index.html", user=user)

    @app.route("/login", methods=["POST"])
    def login():
        import sys

        email = request.form["email"]
        password = request.form["password"]
        user = database.find_user(email)
        sys.stderr.write("email = %s user = %s\n" % (email, user))
        if user is None and email.lower() == "marcallenpage@gmail.com":
            user = database.create_user(email, password, "Marc", 0.0)
            sys.stderr.write("CREATED: email = %s user = %s\n" % (email, user))
        elif user is None:
            return redirect("/#user_not_found")

        response = make_response(redirect("/welcome"))
        response.set_cookie("user_id", str(user.id))
        sys.stderr.write("COOKIE SET\n")
        return response

    @app.route("/restaurant/<restaurant_id>")
    def restaurant(restaurant_id):
        found = database.get_restaurant(restaurant_id)
        if not found:
            return (render_template("404.html", path="???"), 404)
        return render_template("resteraunt.html", restaurant=found)

    @app.route("/welcome")
    def welcome():
        user_id = request.cookies.get("user_id")
        import sys

        sys.stderr.write("user_id = %s\n" % (user_id))
        user = database.get_user(int(user_id)) if user_id is not None else user_id
        return render_template("welcome.html", user=user)

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
