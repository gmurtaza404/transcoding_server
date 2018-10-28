"""
    Utilities
        1. get_directory(path_to_file) returns path to the parent directory
        2. get_file_size(path_to_file) return size of file in bytes
        3. compress_image(path_to_image, path_to_output, quality) generates a new image on the given path with given quality parameter

"""
import os

def get_directory(path_to_file):
    path_list = path_to_file.split("/")
    path_list.pop()
    
    if len(path_list):
        path_list[len(path_list)-1] = path_list[len(path_list)-1] + "/"
    
    directory_to_write_in = "/".join((path_list))
    return directory_to_write_in

def find_file_sizes(path_to_file):
    return os.path.getsize(path_to_file)


def compress_image_x_percent(path_to_file, x):
    directory_to_write_in = get_directory(path_to_file)
    file_name = path_to_file.split("/")[-1]
    output_file_name = "{}_{}".format(x, file_name)
    path_to_output = directory_to_write_in + output_file_name
    compress_image(path_to_file,path_to_output,x)
    return path_to_output



def compress_image(path_to_image, path_to_output, quality):
    file_extension = path_to_image.split(".")[-1]
    if file_extension == "png":
        generate_images_pngquant(path_to_image,path_to_output,quality)
    else:
        generate_images_convert(path_to_image,path_to_output,quality)

def generate_images_convert(path_to_image, path_to_output ,quality):
    if not os.path.exists(path_to_output):
        os.system("convert {} -quality {} {}".format(path_to_image, quality, path_to_output))
def generate_images_pngquant(path_to_image, path_to_output ,quality):
    if not os.path.exists(path_to_output):
        os.system("pngquant {} --quality={}-{} -o{}".format(path_to_image, quality, quality ,path_to_output))
