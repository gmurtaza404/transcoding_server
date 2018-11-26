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
    return float(os.path.getsize(path_to_file))


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


def update_extension(path_to_file, new_ext):
    path_to_file = path_to_file.split(".")
    path_to_file[-1] = new_ext
    path_to_file = ".".join(path_to_file)
    return path_to_file


def val_in_range(low,high):
	val_range = range(1,101)
	if (high in val_range) and (low in val_range):
		return (low+high)/2
	elif high in val_range:
		return high
	elif low in val_range:
		return low
	

def load_json_file(path_to_file):
	json_dict = {}
	with open(path_to_file, "rb") as f:
		json_dict = json.loads(f.read())
	return json_dict

def fix_file_name(name_of_file):
    # removes conditional stuff from image name
    new_name = name_of_file.split("?")[0]
    os.system("mv {} {}".format(name_of_file, new_name))

def list_folders_in_a_directory(path_to_directory):
    all_items = os.listdir(path_to_directory)
    return map(lambda y: os.path.join(path_to_directory, y),filter(lambda x: os.path.isdir(os.path.join(path_to_directory, x)), all_items))