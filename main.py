import datetime
from sys import argv
import requests
import json
import secrets


URL = "https://www.strava.com/api/v3/segments/"
STARRED_URL = "https://www.strava.com/api/v3/segments/starred??page=1&per_page=30"
ACCESS_TOKEN = secrets.TOKEN
params = {
    "access_token": ACCESS_TOKEN
}

#TEST Segment = 8087230
script = argv
prompt = 'Enter Segment ID > '
segment_id = input(prompt).lower()


def get_starred():
    r = requests.get(STARRED_URL, params=params)
    r.raise_for_status()
    starred_data = r.json()
    #formatted = json.dumps(starred_data, indent=4, sort_keys=True)
    # print(formatted)
    for data in starred_data:
        kom = data["athlete_pr_effort"]["is_kom"]
        pr_time = data["pr_time"]
        pr_string = str(datetime.timedelta(seconds=pr_time))
        if kom:
            KOM = "👑"
        else:
            KOM = ""
        print(f"{data['id']} - {data['name']} {KOM} - PR = {pr_string}")


def get_data():
    r = requests.get(URL + segment_id, params=params)
    r.raise_for_status()
    segment_data = r.json()
    name = segment_data['name']
    kom = segment_data['xoms']['overall']
    pr_time = segment_data['athlete_segment_stats']['pr_elapsed_time']
    pr_string = str(datetime.timedelta(seconds=pr_time))
    print(f"{name} - KOM: {kom} - PR {pr_string}")


if segment_id == 'starred':
    get_starred()
else:
    get_data()


# TODO - split overall time and multiply first by 60 to get seconds + seconds - then divide by PR to get % behind
#TODO abstract into classes
#TODO: TRY STATEMENTs
