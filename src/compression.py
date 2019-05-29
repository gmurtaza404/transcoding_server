import os
from utilities import *
WEBP_ENABLED = True

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif"]


def quality_binary_search(path_to_image, path_to_tmp,percentage, low, high):
    if high<low:
        return val_in_range(low,high)
    
    mid = int((low+high)/2)
    rate = compress_image(path_to_image, path_to_tmp, mid)
    os.system("rm {}".format(path_to_tmp))
    
    size_comp = size_comparison(percentage,rate)
    if size_comp==0: #size in range
		return mid
    elif size_comp==-1: #size too low
		return quality_binary_search(path_to_image,path_to_tmp,percentage,mid+1,high)
    elif size_comp==1: #size too high
		return quality_binary_search(path_to_image,path_to_tmp,percentage,low,mid-1)

def get_output_file_name(path_to_file, x):
    directory_to_write_in = get_directory(path_to_file)
    file_name = path_to_file.split("/")[-1]
    output_file_name = "{}_{}".format(x, file_name)
    path_to_output = directory_to_write_in + output_file_name
    return path_to_output


def compress_image_by_percentage(path_to_image, percentage):
    path_to_output = get_output_file_name(path_to_image, percentage)
    path_to_output = update_extension(path_to_output, "webp")
    
    path_to_tmp = path_to_output.split("/")
    path_to_tmp[-1] = "temp.webp"
    path_to_tmp = "/".join(path_to_tmp)

    file_extension = path_to_image.split(".")[-1]
    if file_extension not in SUPPORTED_FORMATS:
        print "Not compressing file {} because format is not supported!".format(path_to_image.split("/")[-1])
        return path_to_image
   
    if os.path.exists(path_to_output):
        return path_to_output
    
    if not(0 <= percentage <= 100):
		print "Error: Percentage must be in the range {} to {}".format(0,100)
		sys.exit(1)
    quality_level = quality_binary_search(path_to_image,path_to_tmp,percentage,1,100)
    achieved_compression = compress_image(path_to_image,path_to_output, quality_level)
    
    print "Achieved {} percent compression at quality {}".format(achieved_compression, quality_level)
    return path_to_output



def change_image_format(path_to_image, output_format):
    path_to_output = path_to_image
    path_to_output = update_extension(path_to_output, output_format)
    
    file_extension = path_to_image.split(".")[-1]
    
    if file_extension not in SUPPORTED_FORMATS:
        print "Not chaninging file {} because format is not supported!".format(path_to_image.split("/")[-1])
        return path_to_image

    if os.path.exists(path_to_output):
        return path_to_output
    
    try:
        if output_format == "webp":
            convert_to_webp(path_to_image, path_to_output)
        else:
            convert_format(path_to_image, path_to_output)
    except:
        print "Failed to convert format"
        return path_to_image
    return path_to_output


def change_image_size(path_to_image, resize_percentage):
    file_extension = path_to_image.split(".")[-1]
    path_to_output = get_output_file_name(path_to_image, resize_percentage)
    try:
        if file_extension == "webp":
            resize_image_cwebp(path_to_image, path_to_output, resize_percentage)
        else:  
            resize_image_convert(path_to_image, path_to_output, resize_percentage)
    except:
        print "Failed to resize!"
        return path_to_image
      
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
    
    return (1- (find_file_size(path_to_output)/find_file_size(path_to_image)) )*100






def convert_format(path_to_image, path_to_output):
    if not os.path.exists(path_to_output):
        os.system("convert {} {}".format(path_to_image, path_to_output))

def convert_to_webp(path_to_image, path_to_output):
    if not os.path.exists(path_to_output):
        file_extension = path_to_image.split(".")[-1]
        if file_extension not in "gif":
            os.system("cwebp {} -o {}".format(path_to_image, path_to_output))
        else:
            os.system("gif2webp {} -o {}".format(path_to_image, path_to_output))


def size_comparison(target_percentage,actual_percentage):
	slack = 1 #percent
	percent_upper = target_percentage+slack
	percent_lower = target_percentage-slack
	if actual_percentage<percent_lower: #not enough size reduction achieved
		return  1
	elif actual_percentage>percent_upper: #too much reduction achieved
		return -1
	else:
		return 0



def generate_image_cwebp(path_to_image, path_to_output, quality):
    if not os.path.exists(path_to_output):
        os.system("cwebp -q {} {} -o {} -quiet".format(quality, path_to_image, path_to_output))

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

def resize_image_convert(path_to_image, path_to_output, resize_percentage):
    if not os.path.exists(path_to_output):
        os.system("convert {} -resize {} {}".format(path_to_image, resize_percentage, path_to_output))

def resize_image_cwebp(path_to_image, path_to_output, resize_percentage):
    if not os.path.exists(path_to_output):
        os.system("cwebp {} -resize {} -o {}".format(path_to_image, resize_percentage, path_to_output))