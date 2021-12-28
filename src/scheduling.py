#!/usr/bin/env python3

import argparse
import os
from flask import Flask, render_template, request, redirect


def create_app(state_dir, source_dir, template_dir):
    app = Flask(__name__, static_folder=source_dir,
                template_folder=template_dir)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form['email']
        password = request.form['password']
        return redirect('/welcome')

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return (render_template('404.html', path='???'), 404)

    return app


def parse_args():
    """ Parses and returns command line arguments.
    """

    parser = argparse.ArgumentParser(description='Schedule maker.')
    parser.add_argument('-p', '--port', type=int, default=8000,
                        help='The port to listen on (default 8000)')
    parser.add_argument('-s', '--storage', type=str, default="storage",
                        help='Directory that stores state information')
    parser.add_argument('-u', '--ui', type=str, default="ui",
                        help='Path to the directory with ui files.')
    parser.add_argument('-d', '--debug', default=True,
                        help='Run debug server.')
    args = parser.parse_args()

    return args


def main():
    """ Entry point. Loop forever unless we are told not to.
    """

    args = parse_args()
    app = create_app(args.storage, args.ui, os.path.join(args.ui, 'template'))
    app.run(host='0.0.0.0', debug=args.debug, port=args.port)


if __name__ == '__main__':
    main()
