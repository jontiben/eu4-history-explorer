import imageio.v2 as imageio
import os
from datetime import datetime

image_folder = "saved_maps"
fps = 10

video_name = None
unordered_files = []

print(f"[{datetime.now().time()}] Indexing image directory...")
file_count = 0
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        if video_name is None:
            video_name = filename.split(".")[0]
        file_count += 1
        unordered_files.append((os.path.join(image_folder, filename), os.path.getctime(os.path.join(image_folder, filename))))

unordered_files.sort(key=lambda f: f[1])
filenames = []
for file in unordered_files:
    filenames.append(file[0])

print(f"[{datetime.now().time()}] imageio compiling video...")
imageio_writer = imageio.get_writer(f"saved_videos/{video_name}.mp4", fps=fps)
print("Completion:")
for f, filename in enumerate(filenames):
    percentage = round(f/file_count * 100.0, 2)
    print(f"[{datetime.now().time()}]     {str(percentage)}" + '0' * (2 - len(str(percentage).split('.')[1])) + f"% - {filename}")
    imageio_writer.append_data(imageio.imread(filename))
imageio_writer.close()
print(f"[{datetime.now().time()}] 100% - Compilation complete, video saved.")
print(f"Saved video to saved_videos/{video_name}.mp4")