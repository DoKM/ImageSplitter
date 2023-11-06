
import os
from itertools import product
from PIL import Image
Image.MAX_IMAGE_PIXELS = None



def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def ask_for_number():
    while True:
        try:
            number = int(input())
            break
        except ValueError:
            print('Please enter a valid number')
    return number

imagesFolder = make_folder('images')
outputFolder = make_folder('output')

# list all images in the images folder
images = os.listdir(imagesFolder)
# filter any files that do not have a common image extension
images = [image for image in images if image.endswith(('jpg', 'png', 'jpeg'))]

# ask the user which image they want to select
# Loop through the images and print them out with a index number
selectedImage = None
while selectedImage is None:
    for index, image in enumerate(images):
        print(f'[{index}] {image}')
    print('Please select an image to convert:')
    selectedImageIndex = ask_for_number()
    if(selectedImageIndex >= len(images)):
        print('Please enter a valid number')
    else:
        selectedImage = images[selectedImageIndex]

# get the selected image
# print the selected image
print(f'You selected: {selectedImage}')
# load the selected image into memory
print(os.path.join(imagesFolder, selectedImage))

image = Image.open(os.path.join(imagesFolder, selectedImage))

# ask the min depth number
print('Please enter the minimum depth:')
minDepth = ask_for_number()
print('Please enter the maximum depth:')
maxDepth = ask_for_number()

resolution = None
resolutions = [1024, 2048, 4096]
while resolution is None:
    for index, res in enumerate(resolutions):
        print(f'[{index}] {res}')
    print('Please select an resolution:')
    resolutionIndex = ask_for_number()


    # get the selected image
    if(resolutionIndex >= len(resolutions)):
        print('Please enter a valid number')
    else:
        resolution = resolutions[resolutionIndex]
# print the selected image
print(f'You selected: {resolution}')

# strip extension from selectedImage
selectedImageName = os.path.splitext(selectedImage)[0]
selectedImageExtension = os.path.splitext(selectedImage)[1]

# create a folder for the selected image in the output folder
imageOutputFolder = make_folder(os.path.join(outputFolder, selectedImageName))
# split the image into multiple images

# split the images based on depth
# a depth of 0 won't split the image at all
# a depth of 1 will split the image into 4 images
# a depth of 2 will split the image into 16 images
# etc...

# the images will be saved in the imageOutputFolder/{depth}/{row}/{column}.{extension}

def tile(imgage, name, ext, base_dir, rows_cols):
    width, height = image.size
    tile_width = width // rows_cols
    tile_height = height // rows_cols
    # calculate the amount of tiles in total
    total_tiles = rows_cols * rows_cols
    

    for i in range(rows_cols):
        i_dir = make_folder(os.path.join(base_dir, str(i)))
        for j in range(rows_cols):
            # print a loading bar for the current operation
            print(f'[{i * rows_cols + j + 1}/{total_tiles}]', end='\r')
            left = j * tile_width
            upper = i * tile_height
            right = left + tile_width
            lower = upper + tile_height

            tile_img = image.crop((left, upper, right, lower))

            # Resize the cropped image to 4096 without losing the aspect ratio
            max_size = (1024, 1024)
            tile_img.thumbnail(max_size)

            out = os.path.join(i_dir, f'{j}{ext}')
            tile_img.save(out)

    
for depth in range(minDepth, maxDepth + 1):
    print(f'Creating depth {depth}...')
    depthOutputFolder = make_folder(os.path.join(imageOutputFolder, str(depth)))
    tile(image, selectedImageName, '.png', depthOutputFolder, 2**depth)

# create a json file called info.json in the imageOutputFolder
# the data in the json file should be:
# {
#    "mapWidth": width of the original image,
#    "mapHeight": height of the original image,
#    "xOffset": 0,
#    "yOffset": 0,
#    "minDepth": minDepth,
#    "maxDepth": maxDepth,
#    "maxZoom": 100,
# }

data = {
    "mapWidth": image.width,
    "mapHeight": image.height,
    "xOffset": 0,
    "yOffset": 0,
    "minDepth": minDepth,
    "maxDepth": maxDepth,
    "maxZoom": 100,
    "extension": selectedImageExtension
}

import json
with open(os.path.join(imageOutputFolder, 'info.json'), 'w') as f:
    json.dump(data, f, indent=4)
    