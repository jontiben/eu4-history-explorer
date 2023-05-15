import imageio.v2 as imageio
import os

image_folder = "saved_maps"
frame_duration = 0.1

images = []
gif_name = None
filenames = []

print("Indexing image directory...")
file_count = 0
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        if gif_name is None:
            gif_name = filename.split(".")[0]
        file_count += 1
        filenames.append(os.path.join(image_folder, filename))
print("imageio compiling gif...")
print("Completion:")
for f, filename in enumerate(filenames):
    percentage = round(f/file_count * 100.0, 2)
    print(f"{percentage}% - {filename}")
    images.append(imageio.imread(filename))

print("100% - Compilation complete")
print("Saving gif... (this may take a while)")
imageio.mimsave(f"saved_videos/{gif_name}.gif", images, duration=frame_duration)
print(f"Complete, saved gif to saved_videos/{gif_name}.gif")

