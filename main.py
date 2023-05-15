import save_file_reader
import render_map
import province_mapping
from defines import *
import text_handling_functions
from PIL import Image, ImageDraw

#def handle_resize(out_canvas, image):
#    image = image.zoom((int(out_canvas.winfo_width()), int(out_canvas.winfo_width() * RATIO)), resample=Image.NEAREST)
#    out_canvas.create_image(0, 0, image=image, anchor=tkinter.NW)

def eu4_map_generator(path):
    print(f"Loading {path}")
    #path = path.replace("\\", "\\\\")
    print("Reading save file...")
    reader_out = save_file_reader.get_province_data(path)
    provinces = reader_out[0]
    colonial_colors = reader_out[1]
    print("Mapping pixels...")
    province_pixel_mapping = province_mapping.get_pixel_mappings()
    quit = False
    while not quit:
        #continuing = input("generate > ")
        #if continuing == "quit":
        #    quit = True
        #    return
        for i in range(1444, 1820, 1):
            next_date = f"{i}.11.12"
            print(f"Loading {next_date}...")
            mode = "owner"
            if text_handling_functions.is_date(next_date):
                out_map = render_map.render_to_date(next_date, province_pixel_mapping, provinces, colonial_colors, mode=mode)
                draw_map = ImageDraw.Draw(out_map)
                draw_map.rectangle((0, PROVINCE_MAP_HEIGHT - 25, 120, PROVINCE_MAP_HEIGHT), fill=C_WHITE)
                draw_map.text((20, PROVINCE_MAP_HEIGHT - 20), f"Date: {next_date}", fill=(0, 0, 0))
                #out_map.show()
                formatted_date = next_date.replace(".", "_")
                out_map.save(f"saved_maps/map_{mode}_{formatted_date}.png")
            quit = True

        #out_map = render_map.render_to_date("1550.1.1", province_pixel_mapping, provinces, colonial_colors)


eu4_map_generator(r"FILE PATH HERE")