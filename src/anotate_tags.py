import os
from utilities import find_file_size
"""
    given a beautiful soup object this script anotates.
    Script:
        mem_footprint  # Default is -1
        function       # Default is no_function
        above_the_fold # True/False Default is True
    Image:
        mem_footprint  # Default is -1
        size           # Default is an empty list, otherwise contains a list of possible sizes
        size_on_page   # default is -1
        above_the_fold # True/False Default is True
"""

def anotate_tag(tag, key, path):
    if key == "script":
        return anotate_script(tag)
    elif key == "img":
        return anotate_image(tag,path)
    else:
        return {"error" : True}

def anotate_script(script_tag):
    ret_anotation = {"mem_footprint":-1, "function": [], "above_the_fold": True}
    # TODO learn how to anotate script tag
    return ret_anotation
def anotate_image(img_tag,path):
    ret_anotation = {"mem_footprint":-1, "size_on_page": -1,"above_the_fold": True}
    try:
        ret_anotation["mem_footprint"] = find_file_size(path + img_tag["src"])
    except OSError:
        ret_anotation["mem_footprint"] = 0
    return ret_anotation
