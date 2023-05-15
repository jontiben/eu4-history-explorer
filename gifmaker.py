import imageio.v2 as imageio
import os
from datetime import datetime

# Lots of color flickering from image compression, you've been warned. 

image_folder = "saved_maps"
frame_duration = 0.1

images = []
gif_name = None
unordered_files = []

print(f"[{datetime.now().time()}] Indexing image directory...")
file_count = 0
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        if gif_name is None:
            gif_name = filename.split(".")[0]
        file_count += 1
        unordered_files.append((os.path.join(image_folder, filename), os.path.getctime(os.path.join(image_folder, filename))))

unordered_files.sort(key=lambda f: f[1])
filenames = []
for file in unordered_files:
    filenames.append(file[0])

print(f"[{datetime.now().time()}] imageio compiling gif...")
print("Completion:")
for f, filename in enumerate(filenames):
    percentage = round(f/file_count * 100.0, 2)
    print(f"[{datetime.now().time()}]     {str(percentage)}" + '0' * (2 - len(str(percentage).split('.')[1])) + f"% - {filename}")
    images.append(imageio.imread(filename))

print(f"[{datetime.now().time()}] 100% - Compilation complete")
print(f"[{datetime.now().time()}] Saving gif... (this may take a while)")
imageio.mimsave(f"saved_videos/{gif_name}.gif", images, duration=frame_duration)
print(f"[{datetime.now().time()}] Complete, saved gif to saved_videos/{gif_name}.gif")

