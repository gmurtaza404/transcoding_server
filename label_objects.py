from bs4 import BeautifulSoup
import sys
import re
import json

"""
    This script gives 2 utilities, one to prettify the htmls, second to lable some specific tags.
    Labeled tags are scripts,images,videos,a and links
"""

# insert value in a list
def insert_dict(dict_arg,key,value):
    if key not in dict_arg:
        dict_arg[key] = []
    
    dict_arg[key] = dict_arg[key] + [value]


def add_rids(regex, html_string_list,html_string,tag_id,id):
    
    list_of_tags = re.findall(regex, html_string)
    for tags in list_of_tags:
        temp_tags = tags
        tags = tags.split(" ")
        if len(tags) == 1:
            tags = tags[0].split(">")
            tags[1] = ">"
        
        try:
            new_tags =  " ".join(tags)
            html_string_list[html_string_list.index(temp_tags)] = new_tags
            insert_dict(tag_id,tags[0][1:],id)
            tags.insert(1, "r_id=\"{}\"".format(id))
            id+= 1
        except ValueError:
            print "found an embedded tag"
                    
    return html_string_list,id

def label_tags(page_path):
    id = 0
    updated_html = ""
    tag_id = {}
    file_name = page_path.split("/")[-1].split(".")[0]
    with open(page_path, "rb") as f:
        html_string = f.read()
        regexes = [re.compile('<script.*?>'),re.compile('<noscript.*?>'), re.compile('<img.*?>'),re.compile('<link.*?>'),re.compile('<video.*?>')]
        html_string_list = html_string.split("\n")
        html_string_list = map((lambda x: x.strip()), html_string_list)
        for regex in regexes:
            html_string_list, id = add_rids(regex,html_string_list,html_string,tag_id,id)
        updated_html = BeautifulSoup(" ".join(html_string_list), 'html.parser').prettify()
    with open("{}_base.html".format(file_name), "wb") as f:
        f.write(updated_html)
    with open("{}_json.json".format(file_name),"wb") as f:
        f.write(json.dumps(tag_id))
    return "{}_base.html".format(file_name), "{}_json.json".format(file_name)
    

def page_pretty(page_path):
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open(page_path, "rb") as f:
        html_string = f.read()
        html_string = BeautifulSoup(html_string, 'html.parser').prettify()
    
    with open(page_path, "wb") as f:
        html_string.encode('ascii', 'ignore').decode('ascii')
        f.write(html_string)


# main for debugging purposes
def main():
    page_name = "Ask.com - What's Your Question_.html"
    page_pretty(page_name)
    label_tags(page_name)



#main()