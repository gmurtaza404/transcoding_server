"""
    Some scripts might require sudo access, so run this script with sudo.
"""
from src import utilities, page_transformations
import os
import socket
import pandas as pd 

"""
    Global Variables
"""
website = "www.synthetic.com"
nonce = "_1_{}".format(0)

path = "./WebPages/{}/index.html".format(website) 
curr_ip = "192.168.1.11"
path_url_list = "/home/fatima/chromium/src/tools/perf/page_sets/top_10_mobile.py"
benchmark_command = "/home/fatima/chromium/src/tools/perf/run_benchmark --browser android-chromium --pageset-repeat 1 memory.top_10_mobile --use-live-sites --output-format=csv"
mv_from = "/home/fatima/chromium/src/tools/perf"
mv_to = "/home/fatima/Documents/sproj/measurement_results/results_telemetry/{}/".format(website)

web_cache = "memory:chrome:renderer_processes:reported_by_chrome:web_cache:effective_size"
renderer_proportional_resident_size = "memory:chrome:renderer_processes:reported_by_os:proportional_resident_size"
browser_proportional_resident_size = "memory:chrome:browser_process:reported_by_os:system_memory:proportional_resident_size"
gpu_proportional_resident_size = "memory:chrome:gpu_process:reported_by_os:system_memory:proportional_resident_size"



results = {
    "noimg":{},
    "25":{},
    "50":{},
    "75":{},
    "fixed":{}
}

def generate_transformed_pages(path_to_index_page):
    os.system("python transformations.py {} fix_img_links fixed_index.html".format(path_to_index_page))
    
    path_to_fixed = path_to_index_page.split("/")
    base_path = path_to_fixed[:]
    base_path.pop()
    base_path.pop(0)
    path_to_fixed[-1] = "fixed_index.html"
    path_to_fixed = "/".join(path_to_fixed)
    base_path = "/".join(base_path)
    
    print path_to_fixed
    # No script 
    os.system("python transformations.py {} no_script fixed_index.html".format(path_to_fixed))
    
    # compression transformations
    os.system("python transformations.py {} no_image noimg_index.html".format(path_to_fixed))
    os.system("python transformations.py {} cmprs_imgs 25_index.html -c 25".format(path_to_fixed))
    os.system("python transformations.py {} cmprs_imgs 50_index.html -c 50".format(path_to_fixed))
    os.system("python transformations.py {} cmprs_imgs 75_index.html -c 75".format(path_to_fixed))
    
    url_list = [
        "\"http://{}:8080/{}/noimg_index.html\"".format(curr_ip, base_path),
        "\"http://{}:8080/{}/25_index.html\"".format(curr_ip, base_path),
        "\"http://{}:8080/{}/50_index.html\"".format(curr_ip, base_path),
        "\"http://{}:8080/{}/75_index.html\"".format(curr_ip, base_path),
        "\"http://{}:8080/{}/fixed_index.html\"".format(curr_ip, base_path)
    ]

    #"\"http://{}:8080/{}/noscript_index.html\"".format(curr_ip, base_path)
    return url_list

def parse_csv_file(mv_to):
    os.chdir(mv_to)
    data = pd.read_csv("results.csv")
    for _, row in data.iterrows():
        if "effective_size" in row['name'] and "renderer_process" in row['name']: 
            field = ":".join(row['name'].split(":")[3:])
            results[row["stories"].split("_")[-3]][field] = int(row['avg'])

def make_csv_of_results():
    df = pd.DataFrame.from_dict(results)
    df.to_csv("{}{}.csv".format(website,nonce))


def driver_function():
    root = os.getcwd()
    url_list = generate_transformed_pages(path)    
    with open(path_url_list, "wb") as f:
        write_string = "URL_LIST = [{}]".format(",".join(url_list))
        f.write(write_string)
    # Run telemetry memory benchmark
    os.system(benchmark_command)
    os.chdir(mv_from)
    os.system("mv results.csv {}".format(mv_to))
    os.chdir(root)



def get_page_img_sizes(path_to_folder):
    results["fixed"]["server_img_size"] = page_transformations.page_stats("{}/fixed_index.html".format(path_to_folder), "a.json")
    results["75"]["server_img_size"] = page_transformations.page_stats("{}/75_index.html".format(path_to_folder), "a.json")
    results["50"]["server_img_size"] = page_transformations.page_stats("{}/50_index.html".format(path_to_folder), "a.json")
    results["25"]["server_img_size"] = page_transformations.page_stats("{}/25_index.html".format(path_to_folder), "a.json")
    results["noimg"]["server_img_size"] = page_transformations.page_stats("{}/noimg_index.html".format(path_to_folder), "a.json")
    os.system("rm a.json")



driver_function()
get_page_img_sizes("./WebPages/{}".format(website))
parse_csv_file(mv_to)
make_csv_of_results()










