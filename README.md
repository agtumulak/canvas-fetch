# canvas-fetch
A thing that syncs all your course files to a local directory using the 
[Canvas LMS API]! Wow!

## Setup
canvas-fetch expects a file named `.canvasfetch` in your home directory. 

[Canvas LMS API]: https://canvas.instructure.com/doc/api/index.html

```json
{
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
