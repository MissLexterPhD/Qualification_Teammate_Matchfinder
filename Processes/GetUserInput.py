import openpyxl
import json
import Processes.TBA_API_stuff


def get_users_input():
    team_key = "frc" + input("Please enter your team number: ").rstrip()  # TODO ensure team number being entered is valid
    # token = input("Please input your TBA access token ")
    with open("token.json", "r") as token_json:
        token = json.load(token_json)
        header = {"X-TBA-Auth-Key": token}
        if token == "No token":
            while 1:
                new_token = input("Please enter your 'The Blue Alliance' developer token: ")
                header["X-TBA-Auth-Key"] = new_token
                response = Processes.TBA_API_stuff.dump_team_event_data(team_key, header)
                print(type(response.status_code))
                if response.status_code == 200:
                    with open("token.json", "w") as file:
                        file.write(json.dumps(new_token))
                    break
    return [team_key, header]


def split(string):
    return [char for char in string]


def get_spreadsheet_dir():
    # create excel file
    wb = openpyxl.Workbook()
    while 1:
        directory = input("Please enter the directory where you would like to save your final spreadsheet: ")
        try:
            x = split(directory)
            if x[-1] == "\\" or x[-1] == "/":
                directory = directory + "Alliance Partner Matches.xlsx"
                wb.save(directory)
            else:
                directory = directory + "/Alliance Partner Matches.xlsx"
                wb.save(directory)
            break
        except IOError:
            print("Directory not found. Please try again")
    return [directory, wb]
