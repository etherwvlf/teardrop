from flask import Flask
from flask import render_template
from flask import request, session, url_for, redirect, abort
import traceback
import sys
import string
from stem.control import Controller
from hashlib import sha224
import random
import datetime
from stem import SocketError
import textwrap
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


chatters = []
global chatlines
chatlines = []

def id_generator(size=6,
                   chars=string.ascii_uppercase + string.digits +
                   string.ascii_lowercase):

    return ''.join(random.choice(chars) for i in range(size))


app.secret_key = id_generator(size=64)


def check_older_than(chat_dic, secs_to_live = 180):
    now = datetime.datetime.now()
    timestamp = chat_dic["timestamp"]
    diff = now - timestamp
    secs = diff.total_seconds()

    if secs >= secs_to_live:
        return True

    return False


def process_chat(chat_dic):

    chats = []
    max_chat_len = 69
    if len(chat_dic["msg"]) > max_chat_len:
        
        for message in textwrap.wrap(chat_dic["msg"], width = max_chat_len):
            partial_chat = {}
            partial_chat["msg"] = message.strip()
            partial_chat["timestamp"] = datetime.datetime.now()
            partial_chat["username"] = session["_id"]
            chats.append(partial_chat)

    else:
        chats = [chat_dic]

    return chats


# Remove headers
@app.after_request
def remove_headers(response):
    response.headers["Server"] = ""
    response.headers["Date"] = ""
    return response


# Empty Index page to avoid Flask fingerprinting
@app.route('/', methods=["GET"])
def index():
    return ('', 200)


@app.route('/<string:url_addition>', methods=["GET"])
def drop(url_addition):

    if url_addition != app.config["path"]:
        return ('', 404)

    if "_id" not in session:
        session["_id"] = id_generator()
        chatters.append(session["_id"])

    if request.method == "GET":
        full_path = app.config["hostname"] + "/" + app.config["path"]
        return render_template("drop.html",
                               hostname=app.config["hostname"],
                               path=app.config["path"])


@app.route('/<string:url_addition>/rooms', methods=["GET", "POST"])
def chat_messages(url_addition):

    global chatlines
    more_chats = False
    if url_addition != app.config["path"]:
        return ('', 404)

    to_delete = []
    c = 0
    for chatline_dic in chatlines:
        if check_older_than(chatline_dic):
            to_delete.append(c)

        c += 1

    for _del in to_delete:
        chatlines.pop(_del)

    if request.method == "POST":

        if request.form["dropdata"].strip():
            
            chat = {}
            chat["msg"] = request.form["dropdata"].strip()
            chat["timestamp"] = datetime.datetime.now()
            chat["username"] = session["_id"]
            chats = process_chat(chat)
            chatlines = chatlines + chats
            chatlines = chatlines[-13:]
            more_chats = True

        return redirect(app.config["path"], code=302)

    return render_template("rooms.html",
                           chatlines=chatlines, num_people = len(chatters))

def main():

    try:
        controller = Controller.from_port()
    except SocketError:
        sys.stderr.write(' * Tor proxy or Control Port not running. Start the Tor Browser or Tor daemon and ensure the ControlPort is open.\n')
        sys.exit(1)
        
    
    print(' * Connecting to tor')
    with controller:
        controller.authenticate()

        # Redirect port 80 to 5000(where Flask runs).
        print(' * Creating teardrop service...')
        result = controller.create_ephemeral_hidden_service({80: 5000}, await_publication = True)

        print(" * New teardrop service started.URL: %s.onion" % result.service_id)
        ###result = controller.create_hidden_service(hidden_service_dir, 80, target_port = 5000)

        if not result:
            print(" * Something went wrong, shutting down")
            ###controller.remove_hidden_service(hidden_service_dir)
            ###shutil.rmtree(hidden_service_dir)

        if result.service_id:
            app.config["hostname"] = result.service_id
            app.config["path"] = id_generator(size = 64)
            app.config["full_path"] = app.config["hostname"] + ".onion" + "/" + app.config["path"]
            print(' * Press ctrl+c to quit')
            print(" * Service address: %s" % app.config["full_path"])
        else:
            print(" * Unable to determine service's hostname")

        try:
            app.run(debug=False, threaded = True)
        finally:

            print(" * Shutting down service")
            controller.remove_ephemeral_hidden_service(result.service_id)

if __name__ == "__main__":
    main()
