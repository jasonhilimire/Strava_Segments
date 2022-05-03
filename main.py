from sys import argv
import requests
import json

URL = "https://www.strava.com/api/v3/segments/"
ACCESS_TOKEN = '9ef9aa44d86bfc935078faf191f273a41298ff61'
params = {
    "access_token": ACCESS_TOKEN
}

script = argv
prompt = 'Enter Segment ID> '
segment_id = input(prompt)

r = requests.get(URL + segment_id, params=params)
r.raise_for_status()
segment_data = r.json()
formatted = json.dumps(segment_data, indent=4, sort_keys=True)
print(formatted)
