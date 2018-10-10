import glob, os,json,shutil
from bs4 import BeautifulSoup
from label_objects import page_pretty,label_tags
from create_web_dirs import create_web_dirs
from choose_ids import choose_ids
import pprint as pp
knap_sack_sizes = [25,50,100,200]


def load_json_file(file_name):
	json_dict = {}
	with open(file_name, "rb") as f:
		json_dict = json.loads(f.read())
	return json_dict
def move_to_folder(soup_html,file_name):
    with open("differential_pages/{}".format(file_name),"wb") as f:
		f.write(str(soup_html))
    
    page_pretty("differential_pages/{}".format(file_name))
def find_and_remove_total(obj_list):
    temp_obj = {}
    for obj in obj_list:
        if obj["id"] == "total":
            temp_obj = obj
    obj_list.remove(temp_obj)
    return temp_obj, obj_list

def lable_dict_objs(obj_dict):
    # assuming this function is in a correct directory
    with open("index_json.json", "rb") as f:
        index_json = json.loads(f.read()) 
        print index_json
        for key in index_json:
            for obj in obj_dict:
               if int(obj["id"]) in index_json[key]:
                    obj["type"] = key
        to_remove = []
        for obj in obj_dict:
            if "type" not in obj:
                to_remove.append(obj)
        
        obj_dict = [x for x in obj_dict if x  not in to_remove]
    return obj_dict

def move_to_server_measurements(soup, val):
	copy_tree("./","/var/www/"+str(val)+".com/public_html/")
	
	if os.path.exists("/var/www/"+str(val)+".com/public_html/index.html"):
		os.remove("/var/www/"+str(val)+".com/public_html/index.html")		
	
	with open("/var/www/"+str(val)+".com/public_html/index.html","wb") as f:
		f.write(str(soup))


def make_differntial_pages(base_page,json_file,maxid_file):
    # assumes the directory has index_base.html and index.json file
    root_directory_local = os.getcwd()
    #loading json file
    json_dict = load_json_file(json_file)
    
    #loading page
    html_string = ""
    with open(base_page, "rb") as f:
		  html_string = f.read()
    
    if not os.path.exists("differential_pages"):
		os.makedirs("differential_pages")
    else:
        shutil.rmtree("differential_pages") 
        os.makedirs("differential_pages")
    #os.chdir("differential_pages")
    #create_web_dirs(maxid_file)
    
    for key in json_dict.keys():
        soup = BeautifulSoup(html_string,"html.parser")
        for value in json_dict[key]:
            element = soup.find(key, r_id=value)
            if element:
				element.decompose()
            move_to_folder(soup,"{}.html".format(value))
            #move_to_server_measurements(soup, val)
            #print element
    os.chdir(root_directory_local)

def fix_knapsack_file():
    # checking if a file with name knapsack exists
    if os.path.exists("knapsack.json"):
        object_dict = {}
        total_obj = {}
        with open("knapsack.json", "rb") as f:
            object_dict =json.loads(f.read())
            total_obj ,object_dict = find_and_remove_total(object_dict)
            object_dict = lable_dict_objs(object_dict)
            for obj in object_dict:
                if float(obj["memory_footprint"]) - float(obj["memory_footprint"]) < 0:
                    obj["memory_footprint"] = 0
                else:
                    obj["memory_footprint"] = float(obj["memory_footprint"]) - float(obj["memory_footprint"])
        #print object_dict, total_obj
        obj_dict = filter((lambda x: (x["memory_footprint"] > 0.0 )), object_dict)
        pp.pprint(object_dict)
        
        #for size in knap_sack_sizes:
        #    selected_ids = choose_ids(object_dict,size)
        #    remove_ids = filter((lambda x: (x not in selected_ids)), object_dict)
        #    remove_ids

def main():
    root_directory = os.getcwd()
    for filename in os.listdir("WebPages"):
        print filename
        os.chdir("{}/WebPages/{}".format(root_directory,filename))
        # find index.html file and prettify it
        page_pretty("index.html")
        base_page, json_file, maxid_file= label_tags("index.html")
        make_differntial_pages(base_page,json_file,maxid_file)
        #fix_knapsack_file()
        os.chdir(root_directory)
    
main()