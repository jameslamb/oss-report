
import json
import re
import requests
from requests.utils import parse_header_links


class GithubClient():
    """
    References:
        https://developer.github.com/v3/#pagination
    """
    events_url = "https://api.github.com/users/{}/events?per_page=100"

    def __init__(self):
        self.event_types = [
            'IssuesEvent',
            'PullRequestEvent',
            'PushEvent',
            'ForkEvent'
        ]

        # Set headers
        self._headers = {}

        # Grabbing auth details
        auth_token = os.environ.get('GITHUB_PAT', None)
        if auth_token is None:
            print("Environment variable GITHUB_PAT not found. Making unauthenticated requests.")
        else:
            print("Found env variable GITHUB_PAT. Making authenticated requests.")
            self._headers['Authorization'] = "token " + auth_token

    def get(self, url):
        """
        Issue an HTTP GET request against the Github API
        """
        res = requests.get(url, headers=self._headers)
        res.raise_for_status()
        return(res)

    def get_events_for_user(self, user):
        """
        'events' are a data source GitHub users to track
        activity by users. Their API only returns the last 90
        days of activity.
        """
        url = self.events_url.format(user)
        events = self._get_all(url)

        # filter to types we care about
        events_filtered = []
        for event in events:
            event_type = event['type']
            if event_type in self.event_types:
                try:
                    parsed = self._parse_event(event)
                except:
                    print("WARNING: could not parse event")
                    print(event)
                    parsed = None
                if parsed is not None:
                    events_filtered.append(parsed)

        return(events_filtered)

    def _get_all(self, url):
        """
        Page with the way Github implemented pagination.
        Returns:
            A list of event dictionaries.
        """

        # Build up results
        results = []

        # start a counter
        page_num = 1
        previous_url = None
        next_url = url
        while True:
            print("Working on page {}".format(page_num))

            # get this page
            self.get(url=next_url)

            # add result to results
            res_list = json.loads(res.text)
            assert isinstance(res_list, list)

            # drop results in our list
            results += res_list

            # get next page url
            link_text = res.headers.get('Link', None)
            if link_text is None:
                print("Only one page of results found")
                break

            # Grab URLs
            next_url = [x['url'] for x in parse_header_links(link_text) if x['rel'] == 'next'][0]
            last_url = [x['url'] for x in parse_header_links(link_text) if x['rel'] == 'last'][0]
            if next_url == last_url:
                break

            page_num += 1

        return(results)

    def _parse_event(self, event):
        """
        Given an event, return the fields we care about:
        * type
        * project_name
        * evidence_link (URL to the PR or issue or commit)
        """

        # default is that we don't know what this is
        out = None

        # TODO (james.lamb@uptake.com):
        # there is def a better way
        event_type = event['type']
        if event_type == 'IssuesEvent':
            # For now, care about issues opened
            if event['payload']['action'] == 'opened':
                out = {
                    "type": event["type"],
                    "repo_name": event['repo']['name'],
                    "evidence_url": event['payload']['issue']['html_url']
                }

        if event_type == 'PullRequestEvent':
            # For now, care about PRs opened
            if event['payload']['action'] == 'opened':
                out = {
                    "type": event["type"],
                    "repo_name": event['repo']['name'],
                    "evidence_url": event['payload']['pull_request']['html_url']
                }

        if event_type == 'PushEvent':
            out = {
                "type": event["type"],
                "repo_name": event['repo']['name'],
                "evidence_url": "{}/commit/{}".format(
                    event['repo']['url'],
                    event['payload']['commits'][0]['sha']
                )
            }

        if event_type == 'ForkEvent':
            out = {
                "type": event["type"],
                "repo_name": event['repo']['name'],
                "evidence_url": event['repo']['url']
            }

        # Always grab the id and created date
        if out is not None:
            out['id'] = event['id']
            out['created_at'] = event['created_at']

        return(out)
