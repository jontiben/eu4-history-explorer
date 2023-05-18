from common_functions import *
from defines import *
from PIL import Image
import random

owner_colors = {"---": (100, 100, 100), "none": (100, 100, 100)}
religion_colors = {}
culture_colors = {}
previous_days = 0
out_map = Image.new("RGB", (PROVINCE_MAP_WIDTH, PROVINCE_MAP_HEIGHT))

def render_to_date(date, province_mapping, provinces, colonial_colors, mode="owner"):
    global previous_days, out_map
    days = date_to_days(date)
    for province in provinces:
        if province.id in province_mapping.keys():
            changed = has_changed(previous_days, days, province, mode)
            new_color = changed
            if province.type == "sea":
                if previous_days != 0:
                    new_color = False
                else:
                    new_color = True
                color = C_OCEAN
            elif province.type == "wasteland":
                if previous_days != 0:
                    new_color = False
                else:
                    new_color = True
                color = C_WASTELAND
            elif changed:
                if mode == "owner":
                    current_owner = contemporary_event(date, province.owner)[1]
                    if current_owner not in owner_colors.keys():
                        if current_owner in colonial_colors.keys():
                            owner_colors[current_owner] = colonial_colors[current_owner]
                        else:
                            owner_colors[current_owner] = get_country_color(get_full_country_name(current_owner))
                    color = owner_colors[current_owner]
                elif mode == "controller":
                    current_owner = contemporary_event(date, province.controller)[1]
                    if current_owner not in owner_colors.keys():
                        if current_owner in colonial_colors.keys():
                            owner_colors[current_owner] = colonial_colors[current_owner]
                        else:
                            owner_colors[current_owner] = get_country_color(get_full_country_name(current_owner))
                    color = owner_colors[current_owner]                    
                elif mode == "religion":
                    current_owner = contemporary_event(date, province.religion)[1]
                    if current_owner not in religion_colors.keys():
                        religion_colors[current_owner] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    color = religion_colors[current_owner]
                elif mode == "culture":
                    current_owner = contemporary_event(date, province.culture)[1]
                    if current_owner not in culture_colors.keys():
                        culture_colors[current_owner] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    color = culture_colors[current_owner]
            if new_color:
                pixels = province_mapping[province.id]
                for pixel in pixels:
                    out_map.putpixel(pixel, color)
    previous_days = days
    return out_map