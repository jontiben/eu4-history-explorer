import imageio.v2 as imageio
import os

image_folder = "saved_maps"
fps = 10

video_name = None
filenames = []

print("Indexing image directory...")
file_count = 0
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        if video_name is None:
            video_name = filename.split(".")[0]
        file_count += 1
        filenames.append(os.path.join(image_folder, filename))
print("imageio compiling video...")
imageio_writer = imageio.get_writer(f"saved_videos/{video_name}.mp4", fps=fps)
print("Completion:")
for f, filename in enumerate(filenames):
    percentage = round(f/file_count * 100.0, 2)
    print(f"{percentage}% - {filename}")
    imageio_writer.append_data(imageio.imread(filename))
imageio_writer.close()
print("100% - Compilation complete, video saved.")
print(f"Saved video to saved_videos/{video_name}.mp4")

