import os,json,urllib,time
from bs4 import BeautifulSoup
from utilities import get_directory,compress_image_x_percent

def remove_images_transform(path_to_file,updated_page_name = "cmprs_img_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("img"):
            tag.extract()
        with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
            fw.write(str(soup))


def remove_videos_transform(path_to_file, updated_page_name = "cmprs_img_index.html"):
    directory_to_write_in = get_directory(path_to_file)
    with open(path_to_file, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("video"):
            tag.extract()
        with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
            fw.write(str(soup))



def fix_img_links(path_to_file):
    directory_to_write_in = get_directory(path_to_file)
    if not os.path.exists("{}downloaded_images".format(directory_to_write_in)):
		os.makedirs("{}downloaded_images".format(directory_to_write_in))
    
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
        
        with open("{}imglink_fixed.html".format(directory_to_write_in),"wb") as fw:
            fw.write(str(soup))
        

def compress_images_transform(path_to_file, compression_rate, updated_page_name = "cmprs_img_index.html"):
    root_directory = os.getcwd()
    directory_to_write_in = get_directory(path_to_file)
    with open(path_to_file, "rb") as f:
        os.chdir(directory_to_write_in)
        soup = BeautifulSoup(f.read(), "html.parser")
        for tag in soup.findAll("img"):
            tag["src"] = compress_image_x_percent(tag["src"], compression_rate)
        os.chdir(root_directory)
        with open("{}{}".format(directory_to_write_in,updated_page_name), "wb") as fw:
            fw.write(str(soup))
    
def main():
    # print "preprocessing images..."
    # root_directory = os.getcwd()
    # os.chdir("./WebPages/www.dawnnews.tv")
    
    # json_file_data = {}
    # with open("index_json.json","rb") as f:
    #     json_file_data = json.loads(f.read())
    # find_images_sizes(json_file_data)

    # os.chdir(root_directory)
    #fix_img_links("./WebPages/www.google.com/index.html")
    #find_image_sizes("./WebPages/www.dawnnews.tv/index_base.html")
    #compress_image_x_percent("./0.3_mb_image.png", 25)

    compress_images_transform("./WebPages/www.google.com/imglink_fixed.html", 50)
    print "done"

main()























