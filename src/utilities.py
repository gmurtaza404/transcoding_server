"""
    Utilities
        1. get_directory(path_to_file) returns path to the parent directory
        2. get_file_size(path_to_file) return size of file in bytes
        3. compress_image_x_percent(path_to_image, path_to_output, quality) generates a new image on the given path with given quality parameter
        4. prettify_html(path_to_page, path_to_output) prettifies the input page. 
        5. knapsack(items, maxweight) function takes, a list of item, where each item should have a "memory_footprint" and a "value" attribute. 
                                      It can have additional attributes, and the resulting list will retain those values. and the second parameter is the maxweight.
                                      Maximum memory the webpage is allowed to consume.
                                      Make sure, that memory footprints and maxweight have same unit.
        6. 
"""
import os,sys,functools32,json
from bs4 import BeautifulSoup
 
def get_directory(path_to_file):
    path_list = path_to_file.split("/")
    path_list.pop()
    
    if len(path_list):
        path_list[len(path_list)-1] = path_list[len(path_list)-1] + "/"
    
    directory_to_write_in = "/".join((path_list))
    return directory_to_write_in

def find_file_size(path_to_file):
    return os.path.getsize(path_to_file)


def compress_image_x_percent(path_to_file, x):
    directory_to_write_in = get_directory(path_to_file)
    file_name = path_to_file.split("/")[-1]
    output_file_name = "{}_{}".format(x, file_name)
    path_to_output = directory_to_write_in + output_file_name
    compress_image(path_to_file,path_to_output,x)
    return path_to_output

def prettify_html(path_to_page, path_to_output):
    reload(sys)
    sys.setdefaultencoding('utf8')
    with open(path_to_page, "rb") as f:
        html_string = f.read()
        html_string = BeautifulSoup(html_string, 'html.parser').prettify()
    
    with open(path_to_output, "wb") as f:
        html_string.encode('ascii', 'ignore').decode('ascii')
        f.write(html_string)

# expects a list of dictionaries and returns a list of dictionaries
def knapsack(items, max_weight, value = "value", weight = "memory_footprint"):
    result = [] # knapsack
    @functools32.lru_cache(maxsize=None)
    def bestvalue(i, j):
        if i == 0: return 0
        value= items[i - 1]["value"]
        weight= items[i - 1]["memory_footprint"]
        if weight > j:
            return bestvalue(i - 1, j)
        else:
            return max(bestvalue(i - 1, j), bestvalue(i - 1, j - weight) + value)

    
    j = max_weight
    result = []
    
    for i in xrange(len(items), 0, -1):
        if bestvalue(i, j) != bestvalue(i - 1, j):
            result.append(items[i - 1])
            j -= items[i - 1]["memory_footprint"]
    result.reverse()
    
    return bestvalue(len(items), max_weight), result


#################################################################################
################### H E L P E R F U N C T I O N S ###############################
#################################################################################
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

def load_json_file(path_to_file):
	json_dict = {}
	with open(path_to_file, "rb") as f:
		json_dict = json.loads(f.read())
	return json_dict