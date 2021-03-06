#TODO Add error handling for bad inputs...
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
                    7. label_objects        -> Give unique ids to all the objects in html
                    8. remove_object_by_rid -> Removes an object with given r_id
                    9. cmprs_img_by_rid     -> Compresses image by a factor x
                    10. get_page_stats      -> Get basic stats of a html page and dumps the data in a .json file.
                    11. rmv_svg             -> Removes SVG format files from the webpage
                    12. change_image_format -> Changes format of all images to a new format
                    13. rsz_imgs            -> Resizes all images in a html pages

            Third Parameter: output_html_name, name of the generated html file.
            
        Optional:
            -c/--compression_rate: Optional parameter to specify the compression rate, for cmprs_img and cmprs_img_by_rid transformation
            -r/--r_id: Required parameter for remove_object_by_rid, this generated a 
            -h/--help: Prints help for the API
            -f/--format New format of the Images, required for the change_image_format transformation
            -r/--resize Resize percentage, required for the rsz_imgs transformation

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
    parser.add_argument("-c", "--compression_rate", type=int, default=80, help= "Compression rate (in case of cmprs_img transform, ignored otherwise. Default value is 80")
    parser.add_argument("-r", "--r_id", type=int, default=-1, help= "r_id of the tag that you want to remove from a labeled html file")
    parser.add_argument("-f", "--format", default="jpg", help= "New Image format")
    parser.add_argument("-rs", "--resize", default="100%", help= "New Image Size")
    
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
    elif args.transformation == "label_objects":
        page_transformations.lable_html_tags(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "remove_object_by_rid":
        page_transformations.remove_element_by_rid(args.path_to_html_file, args.r_id, args.output_html_name)
    elif args.transformation == "cmprs_img_by_rid":
        img_filters.compress_image_by_rid_transform(args.path_to_html_file, args.compression_rate ,args.r_id, args.output_html_name)
    elif args.transformation == "get_page_stats":
        page_transformations.page_stats(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "rmv_svg":
        img_filters.remove_svg_transform(args.path_to_html_file, args.output_html_name)
    elif args.transformation == "change_image_format":
        img_filters.change_image_format_transform(args.path_to_html_file, args.format ,args.output_html_name)
    elif args.transformation == "rsz_imgs":
        img_filters.change_image_size_transform(args.path_to_html_file, args.resize ,args.output_html_name)
    else:
        print "Invalid Transformation"
main()