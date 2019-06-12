import openpyxl
import Constants


def get_users_input():
    team_key = "frc" + input("Please enter your team number: ").rstrip()  # TODO ensure team number being entered is valid
    # token = input("Please input your TBA access token ")
    if Constants.token == "":
        token = input("Please enter your 'The Blue Alliance' developer token: ")
    else:
        token = Constants.token
    header = {"X-TBA-Auth-Key": token}
    return [team_key, token, header]


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
