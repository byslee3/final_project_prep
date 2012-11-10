import json
import math


#############################
####### JSON Requests #######
#############################

def get_set_url(set_id, seo_title):

    # Get the URL for any Polyvore set
    # Will be called by another method that writes the JSON string to a text file

    url_1 = "http://www.polyvore.com/"
    url_2 = "/set?id="
    url_3 = "&.out=json"

    target_url = url_1 + seo_title + url_2 + str(set_id) + url_3

    return target_url


def create_set_file(set_id, seo_title):

    # Grabs the JSON string for any Polyvore set, given the set_id and seo_title

    set_url = get_set_url(set_id, seo_title)
    json_file = urllib.urlopen(set_url)
    json_string = json_file.read()

    # Create a file named after the set and write the JSON string to it

    target_filename = "json-files/set-" + str(set_id) + ".txt"
    target_file = open(target_filename, 'w')
    target_file.write(json_string)
    target_file.close()


def get_set_fans_url(set_id):

    # Open up the relevant JSON file

    pass


####################################
####### Reading stored files #######
####################################

def print_test(d):

    # Just use this for testing and printing out the results
    for key, value in d.iteritems():
        print key
        print value


def get_json_dict(filename):

    f = open(filename)
    json_string = f.read()
    json_dict = json.loads(json_string)
    f.close()

    return json_dict


def get_set_attributes(set_id):

    # Returns the set attributes as a dictionary
    d = {}

    # Open the appropriate JSON file and read from it
    filename = "json-files/set-" + str(set_id) + ".txt"
    polyvore = get_json_dict(filename)

    # Pull set attributes from the JSON dict
    d['set_id'] = polyvore["collection"]["id"]
    d['seo_title'] = polyvore["stream"]["items"][0]["seo_title"]
    d['title'] = polyvore["collection"]["title"]
    d['anchor'] = polyvore["collection"]["embed_anchor"]["anchor"]
    d['set_type'] = polyvore["collection"]["category"]
    d['creator_id'] = polyvore["collection"]["user_id"]
    d['creator_name'] = polyvore["collection"]["user_name"]
    d['created_on'] = polyvore["collection"]["createdon"]
    d['imgurl'] = polyvore["collection"]["imgurl"]
    d['score'] = polyvore["collection"]["score"]
    d['pageviews'] = polyvore["collection"]["pageview"]
    d['num_fans'] = polyvore["fav_count"]

    # Counting only the set items that are clothing/products
    d['num_items_all'] = len(polyvore["overlay_items"])
    d['num_items_valid'] = 0

    for item in polyvore["overlay_items"]:

        if item.get("is_product",0) == 1:

            d['num_items_valid'] += 1

    # Return a dictionary of set attributes
    return d


def get_set_fans(set_id):

    pass

    # open the appropriate JSON file and read from it

    # basically copy all the code from print_data_set()

    # return a linkage table, many to many , of sets to fans

    # in model.py, use this to populate database directly w/o sqlalchemy
    # create new table for this


def get_set_items(set_id):

    pass

    # same as get_set_fans














