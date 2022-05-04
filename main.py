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
# print(formatted)
name = segment_data['name']
kom = segment_data['xoms']['overall']

athlete_PR_min = (segment_data['athlete_segment_stats']['pr_elapsed_time']) // 60
athlete_PR_sec = (segment_data['athlete_segment_stats']['pr_elapsed_time']) % 60

print(f"{name} - KOM: {kom} - PR {athlete_PR_min}:{athlete_PR_sec}")


#TODO: if prompt = starred - print 20 starred segments, by NAME, ID, KOM
# TODO - split overall time and multiply first by 60 to get seconds + seconds - then divid by PR to get % behind
