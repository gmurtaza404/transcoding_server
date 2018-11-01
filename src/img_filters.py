import os,json,urllib,time
from bs4 import BeautifulSoup
from utilities import get_directory,compress_image_x_percent

def remove_images_transform(path_to_file,updated_page_name = "rmv_img_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    html_string = ""
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("img"):
            tag.extract()
        html_string = str(soup)
    
    with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
        fw.write(html_string)


def remove_videos_transform(path_to_file, updated_page_name = "rmv_vid_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    html_string = ""
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("video"):
            tag.extract()
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
        fw.write(html_string)



def fix_img_links(path_to_file,updated_page_name = "link_fix_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    if not os.path.exists("{}downloaded_images".format(directory_to_write_in)):
		os.makedirs("{}downloaded_images".format(directory_to_write_in))
    html_string = ""
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("img"):
            image_link = tag["src"]
            if "https" in image_link or "http" in image_link:
                img_name = image_link.split("/")[-1]
                if img_name not in os.listdir("{}downloaded_images".format(directory_to_write_in)):
                    urllib.urlretrieve(image_link, "{}downloaded_images/{}".format(directory_to_write_in,img_name))
                    time.sleep(2)
                tag["src"] = "downloaded_images/{}".format(img_name)
            else:
                continue
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in,updated_page_name),"wb") as fw:
        fw.write(html_string)
        

def compress_images_transform(path_to_file, compression_rate, updated_page_name = "cmprs_img_index.html"):
    root_directory = os.getcwd()
    directory_to_write_in = get_directory(path_to_file)
    html_string = ""
    with open(path_to_file, "rb") as f:
        os.chdir(directory_to_write_in)
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("img"):
            tag["src"] = compress_image_x_percent(tag["src"], compression_rate)
        os.chdir(root_directory)
        html_string = str(soup)
    with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
        fw.write(str(soup))
    














