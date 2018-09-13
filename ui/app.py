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
stdout.write("Initializing Github client\n")


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    This method accepts resume text and routes it to
    the appropriate location.
    """
    global client

    user = request.args.get('user')
    events = client.get_events_for_user(user)
    assert isinstance(events, list)

    # create the "activity" section
    # TODO:
    # There are definitely more elegant ways to do
    # this and it prolly belongs in the client
    type_map = {
        'IssuesEvent': "issues created",
        'PullRequestEvent': "PRs created",
        'PushEvent': "Commits pushed",
        'ForkEvent': "Repos forked"
    }

    # Denormalize out some summary stats
    activities = {}

    for event in events:
        activity_key = type_map[event["type"]]
        repo = event["repo_name"]
        if activities.get(activity_key, None) is None:
            activities[activity_key] = {
                "count": 1,
                "repos": {
                    repo: 1
                }
            }
        else:
            activities[activity_key]['count'] += 1
            if activities[activity_key]["repos"].get(repo, None) is None:
                activities[activity_key]["repos"][repo] = 1
            else:
                activities[activity_key]["repos"][repo] += 1

    # Turn into a list instead of dict of dicts
    activity_list = []
    for k, v in activities.items():
        x = v.copy()
        x['name'] = k
        activity_list.append(x)

    # Return a comma-delimited list of tokens
    return(jsonify({
        "user": user,
        "events": events,
        "total": len(events),
        "activities": activity_list
    }))


@app.route('/about', defaults={'path': ''})
def about_page(path):
    return render_template("about.html")


@app.route('/home', defaults={'path': ''})
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090)
