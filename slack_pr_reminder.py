#!/usr/bin/python

'''
This script reminds assignee of a pull request to review the PR through
sending message to the assignee's personal Slack channel.
'''

from urllib2 import Request, urlopen
import json

BASE = 'https://github.com/eventmobi/'
PROJECTS = [
    'ansible',
    'flux',
    'analytics_engine',
    'contentmanager',
    'fusion-realtime',
    'messaging',
    'mobileapp',
    'web-applications',
    'cms-facade',
]

repo_urls = [BASE + project + '/pulls' for project in PROJECTS]


def _pulls():
    urls = [url for url in repo_urls]


def _read_pulls(url):
    '''Collect links to open pull requests from repo.'''
    print url
    req = Request(url)
    data = urlopen(req)
    return [p['html_url'] for p in json.loads(data)]


def _post(msg, room, auth, color):
    data = json.dumps({
        'message': msg,
        'message_format': 'text',
        'color': color
    }).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % auth
    }


if __name__ == "__main__":
    _pulls()
