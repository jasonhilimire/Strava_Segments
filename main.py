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
    # print(starred_data)
    sorted_data = sorted(starred_data, key=lambda data: (data["athlete_pr_effort"]["is_kom"], get_percent_behind_kom(
        time_string(get_segment_kom(str(data['id']))), data["pr_time"])))
    for data in sorted_data:
        kom = data["athlete_pr_effort"]["is_kom"]
        pr_time = data["pr_time"]
        pr_string = str(datetime.timedelta(seconds=pr_time))
        seg_id = data['id']
        if kom:
            KOM = "👑"
            behind_perc = "👌"
            target_segment = ""
            print(
                f"{seg_id} - {data['name']} -- KOM = {KOM} - PR = {pr_string}")
        else:
            KOM = get_segment_kom(str(seg_id))
            behind = get_percent_behind_kom(time_string(KOM), pr_time)
            behind_perc = "{:.2%}".format(behind)
            if behind < .05:
                target_segment = "🎯🎯🎯 TARGET 🎯🎯🎯"
            else:
                target_segment = "👷🏻👷🏻 work to do! 👷🏻👷🏻"
            print(
                f"{seg_id} - {data['name']} -- KOM = {KOM} - PR = {pr_string} BEHIND: {behind_perc}  {target_segment}")





def user_prompt():
    prompt = 'Enter Any Segment ID > '
    segment_id = input(prompt).lower()
    return segment_id


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


def time_string(time_kom: str):
    if "s" not in time_kom:
        date_time = datetime.datetime.strptime(time_kom, "%M:%S")
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        return a_timedelta.total_seconds()
    else:
        seconds_only = int(time_kom.strip('s'))
        return seconds_only


def get_percent_behind_kom(kom_time: int, pr_time: int):
    n = kom_time/ pr_time
    x = 1 - n
    return x


get_starred()
get_data(get_segment_data())

