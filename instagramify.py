import os
from PIL import Image
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS
import shutil
import time
import glob
import pathlib
import traceback
from imutils import paths
#import tqdm

#Input folder with pictures to process
fpath = r"D:\OneDrive\Pictures\instagramify"
fpath = pathlib.Path(fpath)

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

SHARP_FACTOR = 1.8
ASPECT_RATIO  = 4/5
HEIGHT = 1350
WIDTH = 1080

def insta_resize(fpath, output_path=None, pano = 0):
    fpath = pathlib.Path(fpath)

    image = Image.open(fpath)
    min_im_size = min(image.size)
    if min_im_size < WIDTH:
        print(f"image too small: {fpath}")

    # print(image.size)
    if (pano is None or pano <2 ) and "-" in fpath.stem[-3:]:
        pano = int(fpath.stem[-1])
        print(pano)

    if pano >1 :
        # print(f"height = {image.size[1]}")
        # print(f"height = {image.size[0]/(ASPECT_RATIO*pano)}")

        height_crop = (image.size[1] - image.size[0]/(ASPECT_RATIO*pano) -5)/2
        box = (0, height_crop,image.size[0] , height_crop + image.size[0]/(ASPECT_RATIO*pano))
        image = image.crop(box)



    imm_aspect_ratio = image.size[0]/image.size[1]
    image.thumbnail((HEIGHT*imm_aspect_ratio, HEIGHT), Image.ANTIALIAS)

    #Apply Sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(SHARP_FACTOR)

    pics = int(image.size[0]/WIDTH)
    width_crop = (image.size[0] - WIDTH*pics )/2

    if output_path is None:
        output_path = fpath.parent / "output"
        output_path.mkdir(exist_ok=True)
    else:
        output_path = pathlib.Path(output_path)
    
    # Look for existing pictures and delete them.
    existing_files = output_path.glob(fpath.stem+"*")
    existing_files = [x for x in existing_files if x.is_file()]
    for f in existing_files:
        f.unlink()


    for p in range(int(image.size[0]/WIDTH)):

        #if image not in the correct aspect ratio, crop
        box = (width_crop + (WIDTH*p), 0, width_crop+ (WIDTH * (p+1) ), HEIGHT)
        image_cropped = image.crop(box)

        if pics>1:
            name_suffix = "_PANO_"
        else:
            name_suffix = ""


        fpath_save = output_path/ f"{fpath.stem}_{WIDTH}_{HEIGHT}{name_suffix}{p+1}{fpath.suffix}"
        image_cropped.save(fpath_save, quality=95, dpi=(72,72))


    image.close()
    #Move processed files to archive.
    archive_folder  = fpath.parent / "archive"
    archive_folder.mkdir(exist_ok=True)
    archive_full_path = archive_folder/fpath.name
    shutil.move(str(fpath),str(archive_full_path))

if __name__=="__main__":

    p = pathlib.Path(fpath).glob('*')
    files = [x for x in p if x.is_file() and x.suffix.lower() in image_types]
    # loop over the input images
    for imagePath in files:
        try:
            insta_resize(imagePath, output_path=None, pano = 0)
        except:
            print(f"Error processing {imagePath}")
