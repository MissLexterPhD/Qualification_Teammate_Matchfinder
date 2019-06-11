"""
intake event and team number, output all the matches with that team's qual alliance partners

result includes:
    match number
    which teams play that match
    what alliance they play in that match
    when your team has a match with them
"""
from __future__ import print_function
import pandas as pd
import numpy as np

import requests
import json
import sys


def get_matches(team_id, event_id):
    return requests.get(url=(url + "/team/" + team_id + "/event/" + event_id + "/matches"), headers=header).json()


def split(string):
    return [char for char in string]


team_key = "frc" + input("Please enter your team number: ").rstrip() # TODO ensure team number being entered is valid
# token = input("Please input your TBA access token ")
token = "uhjNJsj6DFYBJGCDcR4FReJcWXKlRcza6B0VOaijKH5SLkJrurTso1Yg2GERUPer"
url = "https://www.thebluealliance.com/api/v3"
year = "2019"
header = {"X-TBA-Auth-Key": token}


# Get data from TBA API\
try:
    with open("json/events.json", "w") as events:
        json.dump(fp=events, obj=requests.get(url=(url+"/team/"+team_key+"/events/"+year), headers=header).json(), indent=4)
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)


# generate list of events
event_key = ""
try:
    with open("json/events.json", "r") as events:
        data = json.load(events)
        for i in range(len(data)):
            print(str(i+1) + ".")
            print("\tEvent name: " + data[i].get("name") +
                  "\n\tLocation: " + data[i].get("address"))
        event = int(input("\nWhich event would you like to use? ")) - 1
        event_key = data[event].get("key")
except FileNotFoundError:
    print("Event data not found")
    sys.exit(1)


# Go through matches and stuff
try:
    with open("json/matches.json", "w") as matches:
        json.dump(fp=matches, obj=get_matches(team_key, event_key), indent=4)
except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)


# finds alliance partners
last_match = {}
prev_match = 0
with open("json/matches.json", "r") as match_data:
    data = json.load(match_data)
    for i in range(len(data)):
        if data[i].get("comp_level") != "qm":
            continue
        if team_key in data[i].get("alliances").get("blue").get("team_keys"):
            disposable = data[i].get("alliances").get("blue").get("team_keys")
        else:
            disposable = data[i].get("alliances").get("red").get("team_keys")
        disposable.remove(team_key)
        match = data[i].get("match_number")
        for j in range(2):
            last_match[disposable[j]] = match
        prev_match = match
# print("Last matches:")
# for key in sorted(last_match.keys()):
#     print("%s: %s" % (key, last_match[key]))


# get alliance member matches
matches_to_watch = {}
for team in last_match.keys():
    with open("json/teammate_matches.json", "w") as match_data:
        json.dump(fp=match_data, obj=get_matches(team, event_key), indent=4)
    with open("json/teammate_matches.json", "r") as match_data:
        data = json.load(match_data)
        for i in range(len(data)):
            if data[i].get("match_number") == last_match.get(team):
                break
            if data[i].get("comp_level") != "qm":
                continue

            # get rid of "frc" in front
            x = split(team)
            team_no = x[3] + x[4]
            if len(x) == 6:
                team_no += x[5]
            if len(x) == 7:
                team_no += x[5] + x[6]

            if team in data[i].get("alliances").get("blue").get("team_keys"):
                alliance = "blue"
            else:
                alliance = "red"

            if matches_to_watch.get(data[i].get("match_number")) is None:
                matches_to_watch[data[i].get("match_number")] = [[team_no, alliance]]
            else:
                matches_to_watch[data[i].get("match_number")].append([team_no, alliance])
print("\nMatches to watch")
for key in sorted(matches_to_watch.keys()):
    print("%s: %s" % (key, matches_to_watch[key]))

# make end product pretty

# make excel file

