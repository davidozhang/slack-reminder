#!/usr/bin/python

import requests
import getpass

BASE = 'https://api.github.com/repos/Eventmobi/'
PROJECTS = {
    'ansible': '#platform',
    'Flux': '#platform',
    'analytics_engine': '#front-end',
    'contentmanager': '#front-end',
    'fusion-realtime': '#front-end',
    'messaging': '#front-end',
    'mobileapp': '#front-end',
    'web-applications': '#front-end',
    'cms-facade': '#front-end',
}
CHANNEL_MAP = {
    'davidozhang': "@davidzhang",
}
REPO_URLS = {project: BASE + project + '/pulls' for project in PROJECTS}


def map_url(project, number):
    return 'https://github.com/EventMobi/{0}/pull/{1}'.format(project, number)


def pulls(auth):
    text, assignee = None, None
    headers = {'Authorization': 'Bearer {0}'.format(auth)}
    for project, url in REPO_URLS.iteritems():
        try:
            r = requests.get(url, headers=headers)
            data = r.json()
            if len(data) > 0:
                for i in range(len(data)):
                    text = ''.join('<' + map_url(project, data[i]['number']) + '|Click here> to review PR in {0} with title: {1}'.format(project, data[i]['title']))
                    if data[i]['assignee']:
                        assignee = CHANNEL_MAP[data[i]['assignee']['login']]
                    else:
                        assignee = PROJECTS[project]
                    if text is not None and assignee is not None:
                        post(text, assignee)
        except ValueError:
            pass


def post(text, username):
    # find your token https://api.slack.com/web
    payload = """{
        "access_token":"xoxp-2162427386-3360743925-3869996840-aa2c89",
        "text":"%s",
        "username":"slack-pr-reminder-bot",
        "channel": "%s"
    }""" % (text, username)
    r = requests.post(
        'https://hooks.slack.com/services/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',
        payload,
    )
    print r.text

if __name__ == "__main__":
    print pulls(getpass.getpass('Enter your Github OAUTH Key: '))
