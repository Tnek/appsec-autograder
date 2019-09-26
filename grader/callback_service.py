import json
import logging
from flask import Flask, request


app = Flask(__name__)
sessions = {}


@app.route("/cb")
def callback():
    """ Exploits firing will callback here """
    sessid = request.args.get("tid", None)
    testid = request.args.get("tid", None)

    if not sessid or not testid:
        err = "Missing sessid or testid"
        logging.warn(err)
        return err, 403

    if sessid not in sessions:
        sessions[sessid] = []

    sessions[sessid].append(testid)
    return "ok"


@app.route("/grade")
def grade():
    """ Returns summary of callbacks as blob """
    sessid = request.args.get("sid", None)
    if not sessid:
        err = "missing sessid"
        logging.warn(err)
        return err, 403

    ret = sessions.get(sessid, {})
    return json.dumps(ret)


if __name__ == "__main__":
    app.run("127.0.0.1", 31337)
