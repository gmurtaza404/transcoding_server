"""
    This script current supports only removal of javascript from the webpage.
"""
from bs4 import BeautifulSoup

def remove_javascript_transform(path_to_file):
    print "removing javascript from a page"
    path_list = path_to_file.split("/")
    path_list.pop()
    
    if len(path_list):
        path_list[len(path_list)-1] = path_list[len(path_list)-1] + "/"
    
    directory_to_write_in = "/".join((path_list))
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("script"):
            tag.extract()
        
        with open("{}no_js_index.html".format(directory_to_write_in), "wb") as fw:
            fw.write(str(soup))
    