#!/usr/bin/env python

import dateutil.parser
import requests
import json
import logging
from datetime import datetime
from os import makedirs, utime
from os.path import dirname, exists, expanduser, getmtime, join

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


class CanvasSession(requests.Session):

    def __init__(self, base_url='', headers={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.update(headers)
        self.base_url = base_url

    def getjson(self, url, **kwargs):
        response = super().get(self.base_url + url, **kwargs)
        return json.loads(response.content)


with open(expanduser('~/.canvasfetch'), 'r') as f:
    config = json.load(f)
target = expanduser(config['target'])
headers = {'Authorization': 'Bearer {}'.format(config['token'])}

with CanvasSession(base_url=config['base url'], headers=headers) as s:
    courses = s.getjson('/api/v1/courses')
    courses = [c for c in courses if c['course_code'] in config['courses']]
    for course in courses:
        logging.info("Syncing '{}'...".format(course['course_code']))
        folders = s.getjson('/api/v1/courses/{}/folders'.format(course['id']))
        folders = {folder['id']: folder for folder in folders}
        files = s.getjson('/api/v1/courses/{}/files'.format(course['id']))
        for file in files:
            folder = folders[file['folder_id']]
            path = join(
                    target,
                    course['course_code'],
                    folder['full_name'],
                    file['filename'])
            remote_modified = dateutil.parser.parse(file['modified_at'])
            if exists(path):
                local_modified = (
                        datetime
                        .fromtimestamp(getmtime(path))
                        .astimezone(remote_modified.tzinfo))
                if local_modified == remote_modified:
                    continue
            # If this is reached, the file needs to be downloaded
            logging.info("Downloading file '{}'...".format(path))
            if not exists(dirname(path)):
                makedirs(dirname(path))
            with open(path, 'wb') as f:
                f.write(s.get(file['url']).content)
            utime(
                    path,
                    (remote_modified.timestamp(), remote_modified.timestamp()))
