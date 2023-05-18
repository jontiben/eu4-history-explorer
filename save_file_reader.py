from text_handling_functions import *
from defines import *
import common_functions
import codecs
import zipfile
import os


class Province:
    def __init__(self, file_lines, start_point):
        self.name = ""
        self.original_culture, self.original_religion, self.original_owner, self.original_controller = "None", "None", "None", "None"
        self.original_colonizer = None
        self.owner, self.controller, self.religion, self.culture = [], [], [], []
        self.start_point = start_point
        self.history = []
        self.id = get_tag(file_lines[start_point].replace('-', ''))
        if self.id in province_types.keys():
            self.type = province_types[self.id]
        else:
            self.type = "land"
        self.info_lines = define_bracket_block(file_lines, start_point)
        self.get_info()

    def get_info(self):
        history_lines = []
        for l, line in enumerate(self.info_lines):
            tag = get_tag(line)
            if tag == "name" and self.name == "":
                self.name = get_data(line)
            elif tag == "original_culture":
                self.original_culture = get_data(line)
            elif tag == "original_religion":
                self.original_religion = get_data(line)
            elif tag == "original_coloniser":
                self.original_colonizer = get_data(line)
            elif tag == "history":
                history_lines = define_bracket_block(self.info_lines, l)
                for s, sub_line in enumerate(history_lines):
                    if self.type == "land":
                        #if get_tag(sub_line) == "owner":
                        #    self.original_owner = get_data(sub_line) 
                        #elif get_tag(sub_line) == "controller":
                        #    self.original_controller = get_data(sub_line)
                        if is_date(sub_line):
                            next_tag = get_tag(history_lines[s + 1])
                            if next_tag != "advisor":
                                if next_tag in USED_TAGS:
                                    if next_tag == "controller":
                                        self.history.append(
                                            (get_tag(sub_line), get_tag(history_lines[s + 1]), get_data(history_lines[s + 2])))
                                    else:
                                        #print(self.id, sub_line, self.info_lines[s + 1], s)
                                        self.history.append(
                                            (get_tag(sub_line), get_tag(history_lines[s + 1]), get_data(history_lines[s + 1])))
                break
        if history_lines == []:
            return None
        self.serialize_data()

    def serialize_data(self):
        if self.original_colonizer is None:
            self.owner = [(start_date, self.original_owner)]
            self.controller = [(start_date, self.original_controller)]
        else:
            self.owner = [(start_date, "---")]
            self.controller = [(start_date, "---")]
        self.culture = [(start_date, self.original_culture)]
        self.religion = [(start_date, self.original_religion)]
        for entry in self.history:
            if entry[1] == "owner":
                self.owner.append((entry[0], entry[2]))
            elif entry[1] == "controller":
                self.controller.append((entry[0], entry[2]))
            elif entry[1] == "culture":
                if entry[2] != self.culture[-1][1]:
                    self.culture.append((entry[0], entry[2]))
            elif entry[1] == "religion":
                if entry[2] != self.religion[-1][1]: # Prevents duplicate entries
                    self.religion.append((entry[0], entry[2]))
        if len(self.owner) > 1:
            self.controller = [self.controller[0]] + [self.owner[1]] + self.controller[1:]


def get_meta_data(meta_lines):
    meta_data = ["1444.11.11"]
    for line in meta_lines:
        if "date=" in line:
            meta_data[0] = line.replace("date=", "")
            break
    return meta_data

def get_province_data(filename):
    global start_date, province_types, nation_info_locations
    provinces = []
    nation_info_locations = {}
    formed_nations = {}
    try:
        savefile = codecs.open(filename, encoding="latin_1").read()
    except:
        return None
    file_lines = savefile.split("\n")
    if file_lines[0].strip() != "EU4txt":  # Compressed save
        try:
            with zipfile.ZipFile(filename, 'r') as zip:
                zip.extractall()
                savefile = codecs.open("gamestate", encoding="latin_1").read()
                file_lines = savefile.split("\n")
                meta_savefile = codecs.open("meta", encoding="latin_1").read()
                meta_file_lines = meta_savefile.split("\n")
                os.remove("gamestate")
                os.remove("meta")
                os.remove("ai")
                meta_data = get_meta_data(meta_file_lines)
                try:
                    os.remove("rnw.zip")  # Handling random new worlds
                except:
                    pass
            if file_lines[0].strip() != "EU4txt":
                return None
        except Exception as exception:
            return None
    else:
        meta_data = get_meta_data(file_lines)
    province_types = {}
    with open(CLIMATE_DEFS_PATH, 'r') as wasteland_check:
        province_types_check_wasteland = wasteland_check.readlines()
    with open(DEFAULT_MAP_PATH, 'r') as ocean_check:
        province_types_check_ocean = ocean_check.readlines()
    impassable = False
    for line in province_types_check_wasteland:
        if get_tag(line).replace(' ', '') == "impassable":
            impassable = True
        if '}' in line:
            impassable = False
        line = line.strip().split(' ')
        if is_province_id('-'+line[0]):
            for province in line:
                if impassable:
                    province_types[province] = "wasteland"
    ocean = False
    for line in province_types_check_ocean:
        if "sea_starts" in line or "RNW Sea provinces" in line or "lakes" in line or "RNW Lake provinces" in line:
            ocean = True
        if '}' in line or '#' in line:
            ocean = False
        line = line.strip().replace("\t",' ').split(' ')
        if ocean:
            if is_province_id('-'+line[0]):
                for province in line:
                    province_types[province] = "sea"
    for l, line in enumerate(file_lines):
        if get_tag(line) == "start_date":
            start_date = get_data(line)
        if get_tag(line) == "provinces" and '	' not in line:
            for s, sub_line in enumerate(define_bracket_block(file_lines, l)):
                if is_province_id(sub_line):
                    new_province = Province(file_lines, l+s+1)
                    if new_province is not None:
                        provinces.append(new_province)
            # Continue checking colonial nations
        line = line.strip()
        if len(line) == 5:
            if is_created_nation(file_lines[l][1:4]):
                if line[3:5] == "={":
                    if "has_set_government_name" in file_lines[l + 1] or "pillaged_capital_state" in file_lines[l+1] or "government_rank=" in file_lines[l+1]:
                        nation_info_locations[file_lines[l][1:4]] = l
            if is_tag(file_lines[l][1:4]):
                if line[3:5] == "={":
                    tag = file_lines[l][1:4]
                    latest_date = "1.1.1"
                    for s, sub_line in enumerate(define_bracket_block(file_lines, l)):
                        if is_date(sub_line):
                            latest_date = get_tag(sub_line)
                        if "changed_tag_from" in sub_line:
                            formed_nations[get_data(sub_line)] = (tag, latest_date)
                            break

    colonial_colors = {}
    for entry in nation_info_locations:
        colonial_color = [255, 0, 255]
        colonial_block = define_bracket_block(file_lines, nation_info_locations[entry])
        for l, line in enumerate(colonial_block):
            if "map_color" in line:
                colors = colonial_block[l+1].strip().replace('  ','').split(' ')[:3]
                for c, color in enumerate(colors):
                    colonial_color[c] = int(color)
                break
        colonial_colors[entry] = tuple(colonial_color)

    for p, province in enumerate(provinces):
        for e, event in enumerate(province.owner):
            for key in formed_nations:
                days = common_functions.date_to_days(formed_nations[key][1])
                if event[1] == key:
                    check_days = common_functions.date_to_days(event[0])
                    if e == len(province.owner) - 1:
                        provinces[p].owner = provinces[p].owner + [(formed_nations[key][1], formed_nations[key][0])]
                        provinces[p].controller = provinces[p].controller + [(formed_nations[key][1], formed_nations[key][0])]
                    elif (check_days < days and common_functions.date_to_days(province.owner[e+1]) > check_days):
                        provinces[p].owner = provinces[p].owner[:e+1] + [(formed_nations[key][1], formed_nations[key][0])] + provinces[p].owner[e+1:]
                        provinces[p].controller = provinces[p].controller[:e+1] + [(formed_nations[key][1], formed_nations[key][0])] + provinces[p].controller[e+1:]

    return provinces, colonial_colors, meta_data