from openpyxl.styles import *
import Constants


def split(string):
    return [char for char in string]


def make_pretty_spreadsheet(last_match, matches_to_watch, wb, directory):
    """
    Exactly what the function name says
    """
    sheet = wb.active

    sheet.title = "Matches"
    sheet["A1"] = "Qual:"
    sheet["B1"] = "Blue Alliance"
    sheet["C1"] = "Red Alliance"

    sheet.column_dimensions["A"].width = Constants.qual_col_width
    sheet.column_dimensions["B"].width = Constants.col_width
    sheet.column_dimensions["C"].width = Constants.col_width
    b_highlight = NamedStyle(name="b_highlight")
    r_highlight = NamedStyle(name="r_highlight")
    b_highlight.fill = PatternFill(start_color=Constants.b_color, end_color=Constants.b_color, fill_type="solid")
    r_highlight.fill = PatternFill(start_color=Constants.r_color, end_color=Constants.r_color, fill_type="solid")
    bd = Side(style=Constants.border_style, color=Constants.border_color)
    b_highlight.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    r_highlight.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    wb.add_named_style(b_highlight)
    wb.add_named_style(r_highlight)

    row = 1
    for match in sorted(matches_to_watch.keys()):
        row += 1
        sheet["A" + str(row)] = match
        # TODO sort value into ascending order based on what match they play with your team
        red_teams = ""
        blue_teams = ""
        for value in matches_to_watch.get(match):
            # get rid of "frc" in front
            x = split(value[0])
            team_no = x[3]
            if len(x) == 5:
                team_no += x[4]
            if len(x) == 6:
                team_no += x[5]
            if len(x) == 7:
                team_no += x[5] + x[6]

            thing = ""
            if "red" in value:
                if red_teams != "":
                    thing += ", " + team_no + " (" + str(last_match.get(value[0])) + ")"
                else:
                    thing = team_no + " (" + str(last_match.get(value[0])) + ")"
                red_teams += thing
            else:
                if blue_teams != "":
                    thing += ", " + team_no + " (" + str(last_match.get(value[0])) + ")"
                else:
                    thing = team_no + " (" + str(last_match.get(value[0])) + ")"
                blue_teams += thing

        sheet["B" + str(row)] = blue_teams
        sheet["C" + str(row)] = red_teams
        sheet["B" + str(row)].style = b_highlight
        sheet["C" + str(row)].style = r_highlight
    wb.save(directory)
