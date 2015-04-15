# -*- coding: utf-8 -*-

import json
import requests

BASE = 'https://api.github.com/repos/YOUR_ORGANIZATION/'
PROJECTS = {
    #github_repo_name : slack_channel_name
}
CHANNEL_MAP = {
    #github_user_name : slack_user_name
}
SLACK_URL = ('https://hooks.slack.com/services/123456/789012345/'
             '67890123456')
NOTIFICATION = '<{0}|Click here> to review {1} PR with title: {2}'

class SlackReminder(object):

    def __init__(self, oauth_key):
        self.payloads = []
        self.projects = PROJECTS
        self.channels = CHANNEL_MAP
        self.repos = {p: BASE + p + '/pulls' for p in self.projects}

        self._pulls(oauth_key)

    def _map_url(self, project, number):
        return 'https://github.com/YOUR_ORGANIZATION/{0}/pull/{1}'.format(
            project,
            number,
        )

    def _pulls(self, auth):
        headers = {'Authorization': 'Bearer {0}'.format(auth)}
        for project, url in self.repos.items():
            r = requests.get(url, headers=headers)
            if r.status_code == 401:
                raise Exception('Invalid OAuth Token')
            data = r.json()
            if data is not None and len(data) > 0:
                self._process(data, project)

    def _process(self, data, project):
        for d in data:
            if d['assignee']:
                assignee_data = d['assignee']
                assignee = self.channels[assignee_data['login']]
            else:
                assignee = self.projects[project]
            self._post(
                assignee,
                project=project,
                title=d['title'],
                number=d['number'],
            )

    def _post(self, assignee, project, title, number):
        text = ''.join(
            NOTIFICATION.format(
                self._map_url(project, number),
                project,
                title,
            ),
        )
        # find your token https://api.slack.com/web
        payload = {
            'access_token': 'YOUR_ACCESS_TOKEN',
            'text': text,
            'username': 'slack-pr-reminder-bot',
            'channel': assignee,
        }
        r = requests.post(SLACK_URL, json.dumps(payload))

if __name__ == "__main__":
    s = SlackReminder(getpass.getpass('Enter your Github OAUTH Key: '))
