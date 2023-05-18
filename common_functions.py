import defines
import os
import codecs
from datetime import datetime

def date_conversion(date: str) -> str:
    # Takes a normally-formatted date string and turns it into
    # DD Month YYYY
    if date == "annexed" or date == "unknown":
        return date
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August",
                  "September", "October", "November", "December"]
    date = date.split('.')
    year = date[0]
    month = month_list[int(date[1]) - 1]
    day = date[2]
    return day + " " + month + " " + year


def date_to_days(date: str) -> int:
    if type(date) == type(None):
        return 0
    elif date == "annexed" or date == "unknown":
        return 0
    # Takes in a date (string) formatted like XXXX.XX.XX and converts it to an integer representing the number of
    # days since January 1, AD 1
    try:
        months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31,
                  30]  # January-November, don't need to add December because it's the last month
        date = date.split('.')
        year, month, day = int(date[0]), int(date[1]), int(date[2])
        return (year - 1) * 365 + sum(months[:month]) + day
    except:
        return 0


def days_to_date(days: int) -> str:
    if type(days) == type(None):
        return 0
    try:
        year_comp = int(days / 365) + 1
        year_remainder = days % 365
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31,
          30, 9999]  # January-November, don't need to add December because it's the last month
        month_total = 0
        month_comp = 0
        for m, month in enumerate(months):
            month_total += month
            if month_total >= year_remainder:
                month_comp = m + 1
                month_total = sum(months[:m])
                break
        day_comp = year_remainder - month_total
        return f"{year_comp}.{month_comp}.{day_comp}"
    except:
        return 0    


def contemporary_event(date: str, events: list) -> tuple:
    # Takes in a date and a list of events, and returns the event that is closest to the date
    # If there are no events, returns None
    if len(events) == 0:
        return ("1.1.1", "None")
    days = date_to_days(date)
    output_event = events[0]
    for event in events:
        check_days = date_to_days(event[0]) - 1
        if check_days <= days:
            output_event = event
        else:
            break
    return output_event



tags_dict = {}
def get_full_country_name(tag: str) -> str:
    global tags_dict
    # Takes a three-character tag and returns the full name
    # Case-insensitive
    # KER (Zia) has an incorrect number of spaces in its filename which is why I have to use .split('-')
    name = None
    try:
        if len(tags_dict) == 0:
            tags_countries_file = open(defines.PATH_TO_COUNTRIES_FILE, 'r')
            tc_lines = tags_countries_file.readlines()
            tags_countries_file.close()
            for line in tc_lines:
                if line[0] != '#' and line[0] != '\n':
                    try:
                        new_line = line.strip().split(" = ")[-1]
                        new_line = new_line.replace("\"",'')
                        new_line = new_line.split('/')[1]
                        new_line = new_line.split('.')[0]
                        tags_dict[line[:3]] = new_line
                    except:
                        continue
            name = tags_dict[tag]
        else:
            if tag in tags_dict.keys():
                name = tags_dict[tag]
        if name is None: # Fallback
            for files in os.walk(defines.PATH_TO_BACKUP_COUNTRIES_FOLDER):
                for filename in files[-1]:
                    if filename[:3] == tag.upper():
                        name = filename[:-4].split('-')[1]
                        if name[0] == ' ':
                            return name[1:]
                        return name
        else:
            return name
    except:
        return tag
    return tag



country_colors = {}
def get_country_color(name):
    name = name.lower()
    if name == "none":
        return (100, 100, 100)
    if len(country_colors.keys()) == 0:
        for files in os.walk(defines.PATH_TO_COUNTRIES_SOURCE):
            for filename in files[-1]:
                file = codecs.open(defines.PATH_TO_COUNTRIES_SOURCE + '\\' + filename, encoding="latin_1").read()
                lines = file.split("\n")
                for line in lines:
                    if line[:5] == "color":
                        # This is an awkward way do to this but because the PDX devs are *so bad* at formatting that
                        # this is the simplest way that works
                        line = line.replace("color",'').replace('=','').replace('{','').replace('}','')
                        line = line.strip()
                        line = line.replace("  ", ' ').replace("\t", ' ')
                        line = line.replace("  ", ' ').split(' ')
                        country_colors[filename[:-4].lower()] = (int(line[0]), int(line[1]), int(line[2]))
                        break
    try:
        return country_colors[name]
    except:
        print("Couldn't find color for " + name)
        return (255, 0, 255)



def has_changed(previous_days, days, province, mode):
    if previous_days == 0:
        return True
    if mode == "owner":
        events_list = province.owner
    elif mode == "controller":
        events_list = province.controller
    elif mode == "culture":
        events_list = province.culture
    elif mode == "religion":
        events_list = province.religion
    elif mode == "combined":
        events_list = province.controller
    if len(events_list) == 0:
        return False
    for event in events_list:
        check_days = date_to_days(event[0])
        if (check_days <= days and check_days > previous_days) or (check_days >= days and check_days < previous_days):
            return True
    return False


def log_out(text) -> None:
    print(f"[{datetime.now().time()}] {text}")
