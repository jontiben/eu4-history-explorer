from PIL import Image, ImageDraw
import sys

import save_file_reader
import render_map
import province_mapping
from defines import *
import text_handling_functions
import common_functions
from common_functions import log_out


start_date = None
end_date = None
interval = 365

# ARGUMENTS:
# -nd = no date


#def handle_resize(out_canvas, image):
#    image = image.zoom((int(out_canvas.winfo_width()), int(out_canvas.winfo_width() * RATIO)), resample=Image.NEAREST)
#    out_canvas.create_image(0, 0, image=image, anchor=tkinter.NW)

def eu4_map_generator(path, args):
    log_out(f"Targeting {path}")
    #path = path.replace("\\", "\\\\")
    log_out("Reading savefile")
    reader_out = save_file_reader.get_province_data(path)
    provinces = reader_out[0]
    colonial_colors = reader_out[1]
    meta_data = reader_out[2]
    start_date = meta_data[0]
    end_date = meta_data[0]
    log_out("Mapping pixels...")
    province_pixel_mapping = province_mapping.get_pixel_mappings()
    mode = "owner"
    dates = []
    changed_interval = False
    changed_mode = False
    for arg in args:
        arg = arg.lower()
        # Handling arguments
        if "mode=" in arg:
            temp_mode = arg.replace("mode=","")
            if temp_mode in VALID_MODES:
                mode = temp_mode
        elif "interval=" in arg:
            temp_interval = arg.replace("interval=", "")
            interval_check = text_handling_functions.parse_interval(temp_interval)
            if interval_check is not None:
                changed_interval = True
                interval = interval_check
        elif "mode=" in arg:
            temp_mode = arg.replace("mode=", "")
            if temp_mode in VALID_MODE_INPUTS:
                mode = VALID_MODE_INPUTS[temp_mode]
                changed_mode = True
        elif "mapmode=" in arg:
            temp_mode = arg.replace("mapmode=", "")
            if temp_mode in VALID_MODE_INPUTS:
                mode = VALID_MODE_INPUTS[temp_mode]
                changed_mode = True
        elif text_handling_functions.is_date(arg):
            dates.append(arg)
    single_shot = True
    if len(dates) > 0:
        start_date = dates[0]
        if len(dates) > 1:
            end_date = dates[1]
            single_shot = False
    if single_shot:
        end_date = "99999.12.31"
    log_out("Rendering maps with the following options:")
    if changed_mode:
        print(f"    mapmode: {mode}")
    else:
        print(f"    mapmode: {mode} (default)")

    print(f"    start date: {common_functions.date_conversion(start_date)}")
    if single_shot:
        print(f"    single-shot mode, one output image")
    else:
        print(f"    end date: {common_functions.date_conversion(end_date)}")
        if changed_interval:
            print(f"    interval: {temp_interval} -> {interval} days")
        else:
            print(f"    interval: {interval} (default)")
    image_count = 0
    for i in range(common_functions.date_to_days(start_date), common_functions.date_to_days(end_date) + interval, interval):
        image_count += 1
        next_date = common_functions.days_to_date(i)
        log_out(f"  Rendering {next_date}...")
        if text_handling_functions.is_date(next_date):
            out_map = render_map.render_to_date(next_date, province_pixel_mapping, provinces, colonial_colors, mode=mode)
            draw_map = ImageDraw.Draw(out_map)
            if "-nd" not in args:
                draw_map.rectangle((0, PROVINCE_MAP_HEIGHT - 25, 120, PROVINCE_MAP_HEIGHT), fill=C_WHITE)
                draw_map.text((20, PROVINCE_MAP_HEIGHT - 20), f"Date: {next_date}", fill=(0, 0, 0))
            #out_map.show()
            formatted_date = next_date.replace(".", "_")
            out_map.save(f"saved_maps/map_{mode}_{formatted_date}.png")
        if single_shot:
            break
    log_out(f"Map generation complete, all {image_count} images saved to the saved_maps directory.")


if __name__ == "__main__":
    # Command format:
    # python main.py [FILEPATH] [ARGS]
    if len(sys.argv) == 1:
        print(HELP_TEXT)
        sys.exit()
    first_arg = sys.argv[1]
    if first_arg in HELP_TERMS:
        print(HELP_TEXT)
        sys.exit()
    args = sys.argv[2:]
    eu4_map_generator(first_arg, args)