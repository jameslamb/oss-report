from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from flask import request
import simplejson as json
from sys import stdout

from GithubClient import GithubClient

# render our special templates
app = Flask(__name__,
            static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# Set up client
stdout.write("Initializing client...\n")
client = GithubClient()
global client
stdout.write("Initializing Github client\n")


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    This method accepts resume text and routes it to
    the appropriate location.
    """
    global model

    user = request.args.get('user')
    events = client.get_events_for_user(user)
    assert isinstance(events, list)

    # Return a comma-delimited list of tokens
    return(jsonify({
        "user": user,
        "events": events,
        "total": len(events)
    }))


@app.route('/about', defaults={'path': ''})
def about_page(path):
    return render_template("about.html")


@app.route('/home', defaults={'path': ''})
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("app.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090)
