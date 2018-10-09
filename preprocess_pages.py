import glob, os,json,shutil
from bs4 import BeautifulSoup
from label_objects import page_pretty,label_tags

def load_json_file(file_name):
	json_dict = {}
	with open(file_name, "rb") as f:
		json_dict = json.loads(f.read())
	return json_dict
def move_to_folder(soup_html,file_name):
    with open("differential_pages/{}".format(file_name),"wb") as f:
		f.write(str(soup_html))
    
    page_pretty("differential_pages/{}".format(file_name))


def make_differntial_pages(base_page,json_file):
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
    
    for key in json_dict.keys():
        soup = BeautifulSoup(html_string,"html.parser")
        for value in json_dict[key]:
            element = soup.find(key, r_id=value)
            if element:
				element.decompose()
            move_to_folder(soup,"{}.html".format(value))
            #print element
    os.chdir(root_directory_local)

def main():
    root_directory = os.getcwd()
    for filename in os.listdir("WebPages"):
        os.chdir("{}/WebPages/{}".format(root_directory,filename))
        # find index.html file and prettify it
        if filename == "www.urdupoint.com":
            os.chdir(root_directory)
            continue
        
        page_pretty("index.html")
        base_page, json_file= label_tags("index.html")
        make_differntial_pages(base_page,json_file)

        os.chdir(root_directory)
    



main()