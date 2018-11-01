"""
    This script current supports only removal of javascript from the webpage.
"""
from bs4 import BeautifulSoup
from utilities import get_directory

def remove_javascript_transform(path_to_file, updated_page_name = "cmprs_img_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    html_string = "" 
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("script"):
            tag.extract()
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in, updated_page_name), "wb") as fw:
        fw.write(html_string)
    