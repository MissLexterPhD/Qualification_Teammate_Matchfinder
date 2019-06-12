"""
intake event and team number, output all the matches with that team's qual alliance partners

result includes:
    match number
    which teams play that match
    what alliance they play in that match
    when your team has a match with them
"""
import Constants

from Processes import GetUserInput, TBA_API_stuff, CreateSpreadsheet

a = GetUserInput.get_users_input()
team_key = a[0]
Constants.token = a[1]
url = Constants.url
header = a[2]
year = Constants.year

b = GetUserInput.get_spreadsheet_dir()
directory = b[0]
spreadsheet = b[1]

TBA_API_stuff.dump_team_event_data(team_key, header)

event_key = TBA_API_stuff.choose_event()

TBA_API_stuff.dump_team_matches_at_event(team_key, event_key, header)

last_match = TBA_API_stuff.get_qual_alliance(team_key)

matches_to_watch = TBA_API_stuff.get_teammate_matches(event_key, last_match, header)

CreateSpreadsheet.make_pretty_spreadsheet(last_match, matches_to_watch, spreadsheet, directory)

print("Your Excel sheet has been generated!")
print("Alliance Partner Matches has been saved to: " + directory)
