#!/usr/bin/env python3

""" scheduling restaurant staff
"""

import argparse
import datetime
import os
import platform
import time

from flask import Flask, render_template, request, redirect, make_response

import model
import tests.prepopulate

# TODO: template # pylint: disable=W0511

if platform.system() == "Darwin":
    STORAGE_PATH = os.path.join(
        os.environ["HOME"], "Library", "Preferences", "scheduling.sqlite3"
    )
elif platform.system() == "Linux":
    STORAGE_PATH = os.path.join(os.environ["HOME"], ".scheduling.sqlite3")
elif platform.system() == "Windows":
    STORAGE_PATH = os.path.join(os.environ["APPDATA"], "scheduling.sqlite3")
else:
    STORAGE_PATH = os.path.join(".scheduling.sqlite3")

STORAGE = "sqlite:///" + STORAGE_PATH
USER_ID_COOKIE = "session"
MAXIMUM_FUTURE_DATE_IN_SECONDS = 1 * 365 * 24 * 60 * 60.0


def convert_from_html_date(html_date):
    """Converts dates sent through html forms to dates suitable for the database
    html_date - Date of the format 2021-12-31
    """
    return datetime.datetime.strptime(html_date, "%Y-%m-%d")


def convert_from_html_time(html_time):
    """Converts times sent through html forms to dates suitable for the database
    html_time - Time of the format 9:00 AM
    returns number of minutes since 12:00 AM
    """
    parsed = time.strptime(html_time, "%I:%M %p")
    return parsed.tm_hour * 60 + parsed.tm_min


# R0915: Too many statements (51/50) (too-many-statements)
# R0914: Too many local variables (16/15) (too-many-locals)
def create_app(storage_url, source_dir, template_dir):
    # pylint: disable=R0914,R0915
    """create the flask app"""
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=source_dir,
        template_folder=template_dir,
    )
    database = model.Database(storage_url)

    # Mark: Root

    @app.route("/")
    def home():
        """default location for the server, home"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        return render_template("index.html", user=user)

    # Mark: Generic Actions

    @app.route("/logout")
    def logout():
        """remove user cookie and redirect back to home"""
        response = make_response(redirect("/"))
        response.set_cookie(USER_ID_COOKIE, "", expires=0)
        return response

    @app.route("/login", methods=["POST"])
    def login():
        """Using POST method for Employee login"""
        email = request.form["email"]
        password = request.form["password"]
        user = database.find_user(email)

        if user is None and not database.get_users():
            # Creates Employee in the database if not exists
            user = database.create_user(
                email, password, "Admin", hours_limit=0.0, admin=True
            )
        elif user is None:
            # Redirects the user if not found in the database
            return redirect("/#user_not_found")
        restaurants = {r.id: r for r in user.gm_at}
        restaurants.update(
            {p.role.restaurant.id: p.role.restaurant for p in user.roles}
        )
        if len(restaurants) == 1:
            response = make_response(
                redirect(f"/restaurant/{list(restaurants.values())[0].id}")
            )
        else:
            response = make_response(redirect("/welcome"))
        response.set_cookie(USER_ID_COOKIE, str(user.id), secure=False)
        return response

    # Mark: User Actions

    @app.route("/create_user", methods=["POST"])
    def create_user():
        """Creates Employee"""
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = database.create_user(
            email, password, name, hours_limit=40.0, admin=False
        )
        restaurant = database.get_restaurant(request.form["restaurant_id"])
        if restaurant is not None:
            # Adds Employee to restaurant in the database
            database.add_user_to_restaurant(user, restaurant)

        if not user.password_matches(password):
            return redirect("/#user_account_already_exists")
        if restaurant is None:
            response = make_response(redirect("/welcome"))
        else:
            response = make_response(redirect(f"/restaurant/{restaurant.id}"))
        response.set_cookie(USER_ID_COOKIE, str(user.id), secure=False)
        return response

    @app.route("/set_role_priority", methods=["POST"])
    def set_role_priority():
        """Route to set_role_priority using 'POST'"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        if user is None:
            return (render_template("404.html", path="???"), 404)
        for role in user.roles:
            new_priority = request.form.get(f"{role.id}_priority", None)
            if new_priority is not None:
                role.priority = float(new_priority)
        database.flush()
        restaurant = database.get_restaurant(request.form["restaurant_id"])
        if restaurant is None:
            return redirect("/welcome")

        for role in [p for r in restaurant.roles for p in r.preferences]:
            new_gm_priority = request.form.get(f"{role.id}_gm_priority", None)
            if new_gm_priority is not None:
                role.gm_priority = float(new_gm_priority)
        return redirect(f"/restaurant/{restaurant.id}")

    # Mark: Restaurant Actions

    @app.route("/create_restaurant", methods=["POST"])
    def create_restaurant():
        """Creates a restaurant object"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))

        if user is None or not user.admin:
            # If user is not both EMPLOYEE OR ADMIN
            # then return Error 404 Page
            return (render_template("404.html", path="???"), 404)

        created = database.create_restaurant(request.form["name"])
        return redirect(f"/restaurant/{created.id}")

    @app.route("/restaurant/<restaurant_id>/set_gm", methods=["POST"])
    def set_restaurant_gm(restaurant_id):
        """Sets the gm for a restaurant"""
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
        """Adds restaurant role taking 'restaurant_id' as parameter"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        restaurant = database.get_restaurant(restaurant_id)
        name = request.form["name"]
        required_field_empty = user is None or restaurant is None
        if required_field_empty or restaurant.gm_id != user.id:
            return (render_template("404.html", path="???"), 404)
        database.create_role(restaurant_id, name)
        return redirect(f"/restaurant/{restaurant_id}")

    @app.route("/restaurant/<restaurant_id>/add_availability", methods=["POST"])
    def add_restaurant_availability(restaurant_id):
        """adds user availability for a restaurant"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        restaurant = database.get_restaurant(restaurant_id)
        day_of_week = request.form["day_of_week"]
        priority = request.form["priority"]
        start_date = convert_from_html_date(request.form["start_date"])
        end_date = convert_from_html_date(request.form["end_date"])
        start_time = convert_from_html_time(request.form["start_time"])
        end_time = convert_from_html_time(request.form["end_time"])
        note = request.form["note"]
        if user is None or restaurant is None:
            return (render_template("404.html", path="???"), 404)

        database.create_availability(
            user=user,
            restaurant=restaurant,
            day_of_week=day_of_week,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            priority=priority,
            note=note if note else None,
        )

        return redirect(f"/restaurant/{restaurant_id}")

    # Mark: Actual websites

    @app.route("/welcome")
    def welcome():
        """Fetches Employee from database"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        admin_user = user.admin if user is not None else False
        user_list = database.get_users() if admin_user else []
        if admin_user:
            restaurant_list = database.get_restaurants()
        else:
            restaurants = {r.id: r for r in user.gm_at}
            restaurants.update(
                {p.role.restaurant.id: p.role.restaurant for p in user.roles}
            )
            restaurant_list = list(restaurants.values())
        user_restaurants_by_id = {}
        for role in user.roles if user is not None else []:
            user_restaurants_by_id[role.role.restaurant.id] = role.role.restaurant
        sorted_roles = (
            sorted(user.roles, key=lambda r: r.priority) if user.roles else []
        )
        restaurants = list(user_restaurants_by_id.values())
        for restaurant in restaurants:  # in case any new roles have been added
            database.add_user_to_restaurant(user, restaurant)
        database.flush()
        return render_template(
            "welcome.html",
            user=user,
            user_list=user_list,
            restaurant_list=restaurant_list,
            user_restaurants=restaurants,
            sorted_roles=sorted_roles,
            sessions=", ".join([f"{s:.1f}" for s in database.sessions()]),
        )

    @app.route("/restaurant/<restaurant_id>")
    def restaurant(restaurant_id):
        """Fetches Employee "USER_ID_COOKIE' from database"""
        user = database.get_user(request.cookies.get(USER_ID_COOKIE))
        found = database.get_restaurant(restaurant_id)

        if not found:
            return (render_template("404.html", path="???"), 404)

        admin_user = user.admin if user is not None else False
        user_list = database.get_users() if admin_user else []
        gm_user_roles = [p for r in found.roles for p in r.preferences]
        gm_user_roles.sort(key=lambda r: r.gm_priority)
        user_restaurant_roles = (
            [r for r in user.roles if r.role.restaurant_id == int(restaurant_id)]
            if user is not None
            else []
        )
        user_restaurant_roles.sort(key=lambda r: r.priority)
        return render_template(
            "restaurant.html",
            restaurant=found,
            user=user,
            user_list=user_list,
            user_roles=gm_user_roles,
            user_restaurant_roles=user_restaurant_roles,
            today=time.strftime("%Y-%m-%d"),
            latest_date=time.strftime(
                "%Y-%m-%d", time.localtime(time.time() + MAXIMUM_FUTURE_DATE_IN_SECONDS)
            ),
        )

    @app.errorhandler(404)
    def page_not_found(error):
        """Returns error page 404"""
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
        "-t", "--test", action="store_true", help="Preload data into the database"
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
    if args.test:
        tests.prepopulate.load(args.storage)
    app = create_app(args.storage, args.ui, os.path.join(args.ui, "template"))
    app.run(host="0.0.0.0", debug=args.debug, port=args.port)


if __name__ == "__main__":
    main()
