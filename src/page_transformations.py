import os,json
from bs4 import BeautifulSoup
from utilities import prettify_html,get_directory,fix_file_name
from anotate_tags import anotate_tag


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

"""
<img src="img/1_mb_image_jpeg.jpeg" style="width:100px;height:100px;">
<img src="img/1_mb_image_png.png" style="width:100px;height:100px;">
<img src="img/1_mb_image_gif.gif" style="width:100px;height:100px;">
"""
def page_stats(path_to_page, path_to_json_file):
    directory_to_write_in = get_directory(path_to_page)
    data_list = {"script": {"count":0, "all":[]}, "video":{"count":0, "all":[]}, "img":{"count":0, "all":[]}, "total_size": 0} # this list handles all the entries
    soup = None
    with open(path_to_page, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser") 
    for key in data_list.keys():
        tags = soup.find_all(key)
        for tag in tags:
            try:
                data_list[key]["count"] += 1
                data_list[key]["all"].append(anotate_tag(tag,key,directory_to_write_in))
                #print "tag found"
            except KeyError:
                print "tag not labeled"
    for a in data_list["img"]["all"]:
        data_list["total_size"] += a["mem_footprint"]
    print len(data_list["img"]["all"])

    with open("{}".format(path_to_json_file), "wb") as fw:
        fw.write(json.dumps(data_list))
    return data_list["total_size"]
# def fix_name_of_all_files(path_to_page, updated_page_name):
#     directory_to_write_in = get_directory(path_to_page)
#     html_string = ""
#     with open(path_to_file, "rb") as f:
#         soup = BeautifulSoup(f.read(), "html.parser")
#         for tag in soup.findAll("img"):


