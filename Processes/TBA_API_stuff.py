import requests
import json
import sys
import Constants


def get_matches(team_id, event_id, header):
    return requests.get(url=(Constants.url + "/team/" + team_id + "/event/" + event_id + "/matches"), headers=header).json()


def dump_team_event_data(team_key, header):
    try:
        with open("json/events.json", "w") as events:
            json.dump(fp=events, obj=requests.get(url=(Constants.url+"/team/"+team_key+"/events/"+Constants.year), headers=header).json(), indent=4)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def choose_event():
    try:
        with open("json/events.json", "r") as events:
            data = json.load(events)
            for i in range(len(data)):
                print(str(i + 1) + ".")
                print("\tEvent name: " + data[i].get("name") +
                      "\n\tLocation: " + data[i].get("address"))
            event = int(input("\nWhich event would you like to use? ")) - 1
            return data[event].get("key")
    except FileNotFoundError:
        print("Event data not found")
        sys.exit(1)


def dump_team_matches_at_event(team_key, event_key, header):
    try:
        with open("json/matches.json", "w") as matches:
            json.dump(fp=matches, obj=get_matches(team_key, event_key, header), indent=4)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)


def get_qual_alliance(team_key):
    last_match = {}
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
    return last_match


def get_teammate_matches(event_key, last_match, header):
    matches_to_watch = {}
    for team in last_match.keys():
        with open("json/teammate_matches.json", "w") as match_data:
            json.dump(fp=match_data, obj=get_matches(team, event_key, header), indent=4)
        with open("json/teammate_matches.json", "r") as match_data:
            data = json.load(match_data)
            for i in range(len(data)):
                if data[i].get("match_number") == last_match.get(team):
                    break
                if data[i].get("comp_level") != "qm":
                    continue

                if team in data[i].get("alliances").get("blue").get("team_keys"):
                    alliance = "blue"
                else:
                    alliance = "red"

                if matches_to_watch.get(data[i].get("match_number")) is None:
                    matches_to_watch[data[i].get("match_number")] = [[team, alliance]]
                else:
                    matches_to_watch[data[i].get("match_number")].append([team, alliance])
    return matches_to_watch
