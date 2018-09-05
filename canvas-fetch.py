#!/usr/bin/env python

import dateutil.parser
import requests
import json
from datetime import datetime
from os import makedirs, utime
from os.path import dirname, exists, expanduser, getmtime, join


with open(expanduser('~/.canvasfetch'), 'r') as f:
    config = json.load(f)
config['target'] = expanduser(config['target'])
headers = {'Authorization': 'Bearer {}'.format(config['token'])}

url = 'https://umich.instructure.com/api/v1/courses'
response = requests.get(url, headers=headers)
courses = json.loads(response.content)
courses = [
        course
        for course in courses
        if course['course_code'] in config['courses']]
for course in courses:
    print("Syncing '{}'...".format(course['course_code']))
    url = 'https://umich.instructure.com/api/v1/courses/{}/folders'.format(
            course['id'])
    response = requests.get(url, headers=headers)
    folders = json.loads(response.content)
    for folder in folders:
        url = folder['files_url']
        response = requests.get(url, headers=headers)
        files = json.loads(response.content)
        for file in files:
            remote_modified = dateutil.parser.parse(file['modified_at'])
            # Check if nonexistent or updated recently and request new file if necessary
            path = join(config['target'], course['course_code'], folder['full_name'], file['filename'])
            if exists(path):
                local_modified = (
                        datetime
                        .fromtimestamp(getmtime(path))
                        .astimezone(remote_modified.tzinfo))
                if local_modified == remote_modified:
                    continue
            # If this is reached, the file needs to be downloaded
            print("Downloading file '{}'...".format(path))
            if not exists(dirname(path)):
                makedirs(dirname(path))
            url = file['url']
            response = requests.get(url, headers=headers)
            with open(path, 'wb') as f:
                f.write(response.content)
            utime(path, (remote_modified.timestamp(), remote_modified.timestamp()))
