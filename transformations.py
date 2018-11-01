#TODO Add more transformations, example, fixed high,mid,low quality image transforms.

"""
    Main Driver script that applies desired transformation
    API Parameters
        Required:
            First parameter : path_to_html_file, Reference html file.
            Second parameter: transformation, Which transformation you want to apply.
                Currently supported transformations
                    1. no_script            -> Removes all script tags.
                    2. no_image             -> Removes all images from the html.
                    3. no_video             -> Removes all videos from the html.
                    4. fix_image_links      -> Fixes the "src" attributes of the images.
                    5. cmprs_imgs           -> Compresses all images in a html by a given factor.
                    6. page_pretty          -> Prettify the html of the page. 
                    7. lable_objects        -> Give unique ids to all the objects in html
                    8. remove_object_by_rid -> Removes an object with given r_id

            Third Parameter: output_html_name, name of the generated html file.
            
        Optional:
            -c/--compression_rate: Optional parameter to specify the compression rate, for cmprs_img transformation
            -r/--r_id: Required parameter for remove_object_by_rid, this generated a 
            -h/--help: Prints help for the API
    API Examples
        python transformations.py ./WebPages/www.google.com/index.html cmprs_img -c 25 n_index.html
            This command will generate a page with name "n_index.html" with all its images compressed by a factor of 75.
"""

import argparse
from src import img_filters, script_filters,page_transformations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_html_file", help="Path to the html file onto which you want to apply the transformations.")
    parser.add_argument("transformation", help="Which transformation to apply, no_script, no_img etc...")
    parser.add_argument("-c", "--compression_rate", type=int, default=80, help= "Compression rate (in case of cmprs_img transform, ignored otherwise. Default value is 80", )
    parser.add_argument("output_html_name", help="Path to file where you want to write the transformed html")
    args = parser.parse_args()
    if args.transformation == "no_script":
        script_filters.remove_javascript_transform(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "no_image":
        img_filters.remove_images_transform(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "no_video":
        img_filters.remove_videos_transform(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "fix_img_links":
        img_filters.fix_img_links(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "cmprs_imgs":
        img_filters.compress_images_transform(args.path_to_html_file, args.compression_rate,args.output_html_name)
    elif args.transformation == "page_pretty":
        page_transformations.page_prettify(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "lable_objects":
        page_transformations.lable_html_tags(args.path_to_html_file, args.output_html_name)
    
    else:
        print "Invalid Transformation"
main()