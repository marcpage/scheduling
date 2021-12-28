#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect  # pip3 install flask

def main():
    """ Entry point. Loop forever unless we are told not to.
    """

    args = parse_args()
    app = create_app(args.storage, args.ui, os.path.join(args.ui, 'template'))
    app.run(host='0.0.0.0', debug=True, port=args.port)


if __name__ == '__main__':
    main()
