from flask import Flask, request


app = Flask(__name__)


@app.route("/callback")
def callback():
    log = request.args.get("log", None)


@app.route("/grade")
def grade():
    return ""


if __name__ == "__main__":
    app.run("127.0.0.1", 31337)
