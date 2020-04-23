import flask, os
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/login", methods=['POST'])
def logIn():
    """
    In request we want : mail and the password as it is
    :return: response + wrapper if is ok
    """
    # TODO: this will call logIn from MongoDB and take care for all the possible wrapper context
    pass


@app.route("/register", methods=['POST'])
def register():
    """
    In request we want: name, mail, password
    :return: response + wrapper
    """
    # TODO: this will call register from MongoDB and take care for all the possible wrapper context
    pass


@app.route("/create-poll")
def createPoll():
    """
    In request we want : question, options , named, unique and session id
    :return:
    """
    # TODO: this will call createPoll from MongoDB and take care for all the possible wrapper context
    pass


@app.route("/poll", methods=['GET'])  # This function will use parameters in url
def getPollByID():
    """
    We want session_id in request
    :return:
    """
    poll_id = request.args.get("id")
    # TODO: this will call getPollById from MongoDB and take care for all the possible wrapper context
    pass


@app.route("/vote")  # This function will use parameters in url
def vote():
    """
    In request we want session_id, chosen_option
    :return:
    """
    poll_id = request.args.get("id")
    # TODO: this will call vote from MongoDB and take care for all the possible wrapper context
    pass


@app.route("/results")  # This function will use parameters in url
def results():
    """
    In request we want session_id
    :return:
    """
    poll_id = request.args.get("id")
    # TODO: this will call results from MongoDB and take care for all the possible wrapper context
    pass
