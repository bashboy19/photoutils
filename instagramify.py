import os
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
import time
import glob
import pathlib
import traceback
from imutils import paths
import tqdm
 

ASPECT_RATIO  = 4/5
HEIGHT = 1350
WIDTH = 1080

#Input folder with pictures to process
fpath = r"D:\OneDrive\Pictures\insta_postprocessing\source"

#Output folder where script will save the cropped and resized pictures
output_path = r"D:\OneDrive\Pictures\insta_postprocessing\upload"


fpath = pathlib.Path(fpath)

def insta_resize(fpath, output_path=None, pano = 0):
    fpath = pathlib.Path(fpath)

    image = Image.open(fpath)
    min_im_size = min(image.size)
    if min_im_size < WIDTH:
        print(f"image too small: {fpath}")

    # print(image.size)
    if (pano is None or pano <2 ) and "-" in fpath.stem[-3:]:
        pano = int(fpath.stem[-1])

    if pano >1 :
        # print(f"height = {image.size[1]}")
        # print(f"height = {image.size[0]/(ASPECT_RATIO*pano)}")

        height_crop = (image.size[1] - image.size[0]/(ASPECT_RATIO*pano) -5)/2
        box = (0, height_crop,image.size[0] , height_crop + image.size[0]/(ASPECT_RATIO*pano))
        image = image.crop(box)

    imm_aspect_ratio = image.size[0]/image.size[1]
    image.thumbnail((HEIGHT*imm_aspect_ratio, HEIGHT), Image.ANTIALIAS)

    pics = int(image.size[0]/WIDTH)
    width_crop = (image.size[0] - WIDTH*pics )/2

    for p in range(int(image.size[0]/WIDTH)):

        #if image not in the correct aspect ratio, crop
        box = (width_crop + (WIDTH*p), 0, width_crop+ (WIDTH * (p+1) ), HEIGHT)
        image_cropped = image.crop(box)

        if pics>1:
            name_suffix = "_PANO_"
        else:
            name_suffix = ""
        
        if output_path is None:
            output_path = fpath.parent
        else:
            output_path = pathlib.Path(output_path)
            output_path.mkdir(exist_ok=True)

        fpath_save = output_path/ f"{fpath.stem}_{WIDTH}_{HEIGHT}{name_suffix}{p+1}{fpath.suffix}"

        image_cropped.save(fpath_save, quality=100)


if __name__=="__main__":
    imlist = paths.list_images(fpath)
    # loop over the input images
    for imagePath in tqdm.tqdm(imlist):
        insta_resize(imagePath, output_path=output_path, pano = 0)