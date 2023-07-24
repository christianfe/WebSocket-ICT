from flask import Flask, render_template
import os.path

app = Flask(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        return open("static/"+filename).read()
    except IOError as exc:
        return str(exc)


@app.route('/static/<path:path>')
def get_resource(path):  # pragma: no cover
    return get_file(path)


@app.route('/')
def main():
    d = {}
    d["counter"] = 0
    d["id"] = "0"
    return render_template("home.html", data=d)


if (__name__ == '__main__'):
    app.run()
