import codecs
from PIL import Image
import defines

def get_pixel_mappings():
    pixel_mappings = {}
    '''
    try:
        with open("province_mappings", 'r') as in_file:
            lines = in_file.read().split('\n')
            if len(lines) > 2:
                for line in lines:
                    if len(line) > 0:
                        line = line.split(':')
                        pixel_mappings[line[0]] = []
                        for pixel in line[1].split(';'):
                            if len(pixel) > 0:
                                pixel_mappings[line[0]].append((int(pixel[0]), int(pixel[1])))
                print(pixel_mappings)
                return pixel_mappings
    except:
        pass
    '''
    file = codecs.open(defines.PROVINCE_DEFS_PATH, encoding="latin_1").read()
    file_lines = file.split("\n")
    province_colors = {}
    for line in file_lines:
        line = line.split(';')
        if line[0] != "province" and len(line[0]) > 0:
            province_colors[tuple([int(line[1]), int(line[2]), int(line[3])])] = line[0]
    provinces_map = defines.PROVINCE_MAP
    map_width = provinces_map.size[0]
    provinces_map = list(provinces_map.getdata()) # width 5632 for basegame map
    for p in range(len(provinces_map)):
        coords = (p % map_width, int(p / map_width))
        try:
            if province_colors[provinces_map[p]] in pixel_mappings.keys():
                pixel_mappings[province_colors[provinces_map[p]]].append(coords)
            else:
                pixel_mappings[province_colors[provinces_map[p]]] = [coords]
        except:  # Province doesn't exist in the map
            pass
    '''
    output_file = open("province_mappings", 'w')
    output_file.write("")
    output_file.close()
    output_file = open("province_mappings", 'a')
    out_line = ""
    for key in pixel_mappings.keys():
        out_line += key+':'
        for p in pixel_mappings[key]:
            out_line += str(p[0])+','+str(p[1]) + ";"
        out_line += "\n"
        output_file.write(out_line)
        out_line = ""
    output_file.close()
    '''
    return pixel_mappings
