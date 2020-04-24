import flask, os
from flask import request, jsonify

from MongoDatabase.MongoDB import MongoDB
from MongoDatabase.Wrappers.PollWrapper import PollWrapper
from MongoDatabase.Wrappers.VotesWrapper import VotesWrapper
from model.Poll import getPollFromJson

app = flask.Flask(__name__)
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
database = MongoDB()


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
    try:
        poll_id = request.args.get("id")
        session_id = request.json.get("session_id")
        poll_wrapper: PollWrapper = database.getPollById(poll_id, session_id)
        if not poll_wrapper.userFound:
            return jsonify(response=400, msg="Could not find user with session_id: " + session_id)
        if not poll_wrapper.found:
            return jsonify(response=404, msg="Could not find poll with id: "+poll_id)
        return jsonify(response=200, wrapper=poll_wrapper)
    except:
        return jsonify(response=500, msg="Something went wrong")


@app.route("/vote")  # This function will use parameters in url
def vote():
    """
    In request we want session_id, chosen_option
    :return:
    """
    try:
        poll_id = request.args.get("id")
        session_id = request.json.get("session_id")
        chosen_option = request.json.get("chosen_option")
        vote_wrapper: VotesWrapper = database.vote(poll_id, chosen_option, session_id)
        if not vote_wrapper.userFound:
            return jsonify(response=400, msg="Could not find user with session_id: " + session_id)
        if not vote_wrapper.found:
            return jsonify(response=404, msg="Could not find vote with id: " + poll_id)
        return jsonify(response=200, wrapper=vote_wrapper)
    except:
        return jsonify(response=500, msg="Something went wrong")


@app.route("/results")  # This function will use parameters in url
def results():
    """
    In request we want session_id, last_timestamp
    :return:
    """
    # TODO: this will call results from MongoDB and take care for all the possible wrapper context
    try:
        poll_id = request.args.get("id")
        last_timestamp = request.json.get("last_timestamp")
        session_id = request.json.get("session_id")
        votes_wrapper: VotesWrapper = database.results(poll_id, last_timestamp, session_id)
        if not votes_wrapper.userFound:
            return jsonify(response=400, msg="Could not find user with session_id: " + session_id)
        if not votes_wrapper.found:
            return jsonify(response=404, msg="Could not find poll with id: " + poll_id)
        return jsonify(response=200, wrapper=votes_wrapper)
    except:
        return jsonify(response=500, msg="Some`thing went wrong")
