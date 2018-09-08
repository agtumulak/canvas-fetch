# canvas-fetch
A thing that syncs all your course files to a local directory using the 
[Canvas LMS API]! Wow!

## Pre-Setup
A conda environment file, `canvas-fetch.yml`, is provided to satisfy the two
main dependencies: `requests` and `python-dateutil`.

```console
$ conda env create -f canvas-fetch.yml
```

## Setup
canvas-fetch expects a file named `.canvasfetch` in your home directory. 

[Canvas LMS API]: https://canvas.instructure.com/doc/api/index.html

```json
{
  "base url": "https://umich.instructure.com",
  "target": "~/Documents/School",
  "token": "1770~oqR3HQ70QqESqAC2ky5gni7ltofco9ArSlbnbBKoBO9cMduE9AkTXI2J3XfRwh4A",
  "courses": [
    "NERS 543 001 FA 2018",
    "NERS 521 001 FA 2018"
    ]
}
```

You will have to generate a token in Canvas under _Account > Settings >
Approved Integrations_. Don't share it like I do here.

## Scheduling
The following crontab entry runs canvas-fetch using the correct environment
every 5 minutes:

```
*/5 * * * * /usr/local/miniconda3/envs/canvas-fetch/bin/python /absolute/path/to/canvas-fetch.py >> /tmp/canvas-fetch.log 2>&1
```

Run `tail -f /tmp/canvas-fetch.log` to check that it is running properly.
