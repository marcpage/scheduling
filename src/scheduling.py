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
USER_ID_COOKIE = "session"


# R0915: Too many statements (51/50) (too-many-statements)
def create_app(storage_url, source_dir, template_dir):  # pylint: disable=R0915
    """create the flask app"""
    app = Flask(__name__, static_folder=source_dir, template_folder=template_dir)
    database = model.Database(storage_url)

    @app.route("/")
    def home():
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        return render_template("index.html", user=user)

    @app.route("/logout")
    def logout():
        response = make_response(redirect("/"))
        response.set_cookie(USER_ID_COOKIE, "", expires=0)
        return response

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form["email"]
        password = request.form["password"]
        user = database.find_user(email)
        if user is None and email.lower() == "marcallenpage@gmail.com":
            user = database.create_user(
                email, password, "Marc", hours_limit=0.0, admin=True
            )
        elif user is None:
            return redirect("/#user_not_found")

        response = make_response(redirect("/welcome"))
        response.set_cookie(USER_ID_COOKIE, str(user.id), secure=False)
        return response

    @app.route("/create_user", methods=["POST"])
    def create_user():
        # TODO: make sure the email is unique # pylint: disable=W0511
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = database.create_user(
            email, password, name, hours_limit=40.0, admin=False
        )
        restaurant = database.get_restaurant(request.form["restaurant_id"])
        if restaurant is not None:
            database.add_user_to_restaurant(user, restaurant)
        response = make_response(redirect("/welcome"))
        response.set_cookie(USER_ID_COOKIE, str(user.id), secure=False)
        return response

    @app.route("/restaurant/<restaurant_id>")
    def restaurant(restaurant_id):
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        found = database.get_restaurant(restaurant_id)

        if not found:
            return (render_template("404.html", path="???"), 404)

        admin_user = user.admin if user is not None else False
        user_list = database.get_users() if admin_user else []

        return render_template(
            "restaurant.html", restaurant=found, user=user, user_list=user_list
        )

    @app.route("/create_restaurant", methods=["POST"])
    def create_restaurant():
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))

        if user is None or not user.admin:
            return (render_template("404.html", path="???"), 404)

        created = database.create_restaurant(request.form["name"])
        return redirect(f"/restaurant/{created.id}")

    @app.route("/restaurant/<restaurant_id>/set_gm", methods=["POST"])
    def set_restaurant_gm(restaurant_id):
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        gm_id = request.form["gm_id"]
        general_manager = database.get_user(gm_id)
        if user is None or not user.admin or general_manager is None:
            return (render_template("404.html", path="???"), 404)
        found = database.get_restaurant(restaurant_id)
        found.gm = general_manager
        database.flush()
        return redirect(f"/restaurant/{restaurant_id}")

    @app.route("/restaurant/<restaurant_id>/add_role", methods=["POST"])
    def add_restaurant_role(restaurant_id):
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        restaurant = database.get_restaurant(restaurant_id)
        name = request.form["name"]
        required_field_empty = name is None or user is None or restaurant is None
        if required_field_empty or restaurant.gm_id != user.id:
            return (render_template("404.html", path="???"), 404)
        database.create_role(restaurant_id, name)
        return redirect(f"/restaurant/{restaurant_id}")

    @app.route("/welcome")
    def welcome():
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        admin_user = user.admin if user is not None else False
        user_list = database.get_users() if admin_user else []
        restaurant_list = database.get_restaurants() if admin_user else []
        user_restaurants_by_id = {}
        for role in user.roles if user is not None else []:
            user_restaurants_by_id[role.role.restaurant.id] = role.role.restaurant
        sorted_roles = (
            sorted(user.roles, key=lambda r: r.priority) if user.roles else []
        )
        return render_template(
            "welcome.html",
            user=user,
            user_list=user_list,
            restaurant_list=restaurant_list,
            user_restaurants=list(user_restaurants_by_id.values()),
            sorted_roles=sorted_roles,
        )

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
