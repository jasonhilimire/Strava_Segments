import datetime
from sys import argv
import requests
import secrets


URL = "https://www.strava.com/api/v3/segments/"
STARRED_URL = "https://www.strava.com/api/v3/segments/starred??page=1&per_page=30"
ACCESS_TOKEN = secrets.TOKEN
params = {
    "access_token": ACCESS_TOKEN
}

#TEST Segment = 8087230
script = argv


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
        seg_id = data['id']
        if kom:
            KOM = "👑"
        else:
            KOM = get_segment_kom(str(seg_id))
        print(f"--{seg_id} - {data['name']} -- KOM = {KOM} - PR = {pr_string} --")


def user_prompt():
    prompt = 'Enter Any Segment ID > '
    segment_id = input(prompt).lower()
    return  segment_id

def get_segment_kom(segment_id: int):
    r = requests.get(URL + segment_id, params=params)
    r.raise_for_status()
    segment_data = r.json()
    return segment_data['xoms']['overall']

def get_segment_data():
    segment_id = user_prompt()
    r = requests.get(URL + segment_id, params=params)
    r.raise_for_status()
    segment_data = r.json()
    return segment_data

def get_data(segment_data: dict):
    name = segment_data['name']
    kom = segment_data['xoms']['overall']
    pr_time = segment_data['athlete_segment_stats']['pr_elapsed_time']
    pr_string = str(datetime.timedelta(seconds=pr_time))
    print(f"{name} - KOM: {kom} - PR {pr_string}")
    return kom



get_starred()
get_data(get_segment_data())


# TODO - split overall time and multiply first by 60 to get seconds + seconds - then divide by PR to get % behind
#TODO abstract into classes
#TODO: TRY STATEMENTS
#TODO SHOW KOM TIME FOR STARRED SEGMENTS
