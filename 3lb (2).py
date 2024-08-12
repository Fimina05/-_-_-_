import os
import time
import concurrent.futures
from PIL import Image

INPUT_DIRECTORY = 'D:\\input'
OUTPUT_DIRECTORY = 'D:\\output'
SIZE = (100, 100)

def process_images(image_names):
    for image_name in image_names:
        img = Image.open(os.path.join(INPUT_DIRECTORY, image_name))
        img = img.resize(SIZE)
        img.save(os.path.join(OUTPUT_DIRECTORY, image_name))

def main():
    images = os.listdir(INPUT_DIRECTORY)
    num_threads = 4
    images_per_thread = len(images) // num_threads

    # Один поток
    start_time = time.time()
    process_images(images)
    end_time = time.time()
    print(f"Однопоточная {end_time - start_time} seconds.")

    # Много поток
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(num_threads):
            start = i * images_per_thread
            end = (i + 1) * images_per_thread if i != num_threads - 1 else None
            executor.submit(process_images, images[start:end])
    end_time = time.time()
    print(f"Многопоточная {end_time - start_time} seconds.")

if __name__ == "__main__":
    main()
