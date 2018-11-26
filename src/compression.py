import os
from utilities import *
WEBP_ENABLED = True

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif"]






def compress_image_by_percentage(path_to_image, path_to_output, percentage):
    file_extension = path_to_image.split(".")[-1]
    if file_extension not in SUPPORTED_FORMATS:
        print "Not compressing file {} because format is not supported!".format(path_to_image.split("/")[-1])
        return path_to_image
    if os.path.exists(path_to_output):
        return path_to_output

    













def compress_image(path_to_image, path_to_output, quality):
    file_extension = path_to_image.split(".")[-1]
    if not WEBP_ENABLED:
        if file_extension == "png":
            generate_images_pngquant(path_to_image,path_to_output,quality)
        else:
            generate_images_convert(path_to_image,path_to_output,quality)
    else:
        path_to_output = update_extension(path_to_output, "webp")
        if file_extension == "gif":
            compress_gif_gif2webp(path_to_image, path_to_output, quality)
        else:
            generate_image_cwebp(path_to_image, path_to_output, quality)
    
    return (find_file_size(path_to_output)/find_file_size(path_to_image))*100
































def generate_image_cwebp(path_to_image, path_to_output, quality):
    if not os.path.exists(path_to_output):
        os.system("cwebp -q {} {} -o {}".format(quality, path_to_image, path_to_output))

def compress_gif_gif2webp(path_to_image, path_to_output, quality):
    if not os.path.exists(path_to_output):
        os.system("gif2webp -q {} {} -o {}".format(quality, path_to_image, path_to_output))

def generate_images_convert(path_to_image, path_to_output ,quality):
    if not os.path.exists(path_to_output):
        os.system("convert {} -quality {} {}".format(path_to_image, quality, path_to_output))
def generate_images_pngquant(path_to_image, path_to_output ,quality):
    if not os.path.exists(path_to_output):
        os.system("pngquant {} --quality={}-{} -o{}".format(path_to_image, quality, quality ,path_to_output))
def generate_image_copy(path_to_image,path_to_output):
    os.system("cp {} {}".format(path_to_image, path_to_output))
