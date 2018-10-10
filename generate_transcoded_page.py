"""
    This script assumes that there is a json file available for a given page. Lets say a user wants to fetch, www.google.com page
    there exists a folder with name www.google.com and that folder has the base page with all the elements it need. Also, it has
    a JSON file that contains the information regarding, which tag consumes how much memory.
"""


def generate_transcoded_page(obj_list,page,page_type):
    with open(page, "rb") as f:
        soup = BeautifulSoup(f.read(),"html.parser")
        for obj in obj_list:
            element = soup.find(obj["type"], r_id=obj["id"])
            if element:
				element.decompose()

        with open("{}_index.html".format(page_type), "wb") as fw:
            fw.write(str(soup))

