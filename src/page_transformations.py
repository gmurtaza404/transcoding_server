import os,json
from bs4 import BeautifulSoup
from utilities import prettify_html,get_directory



def lable_html_tags(path_to_page, updated_page_name = "tag_labeled_index.html"):
    directory_to_write_in = get_directory(path_to_page)
    i = 0
    html_string = ""
    with open(path_to_page, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.find_all(['script','img',"video"]):
            tag["r_id"] = str(i)
            i += 1
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
        fw.write(html_string)

def remove_element_by_rid(path_to_page, rid,updated_page_name = "lable_deleted_index.html"):
    directory_to_write_in = get_directory(path_to_page)
    html_string = ""
    with open(path_to_page, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        tag = soup.find(['script', 'img', 'video'], r_id=rid)
        if tag:
			tag.decompose()
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
        fw.write(html_string)

def page_prettify(path_to_page,updated_page_name = "pretty_index.html"):
    directory_to_write_in = get_directory(path_to_page)
    path_to_output = "{}{}".format(directory_to_write_in,updated_page_name)
    prettify_html(path_to_page,path_to_output)
