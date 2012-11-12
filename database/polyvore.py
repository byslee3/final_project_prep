import json
import math
import urllib


TEST1 = "62332524"
TEST2 = "62652167"
TEST3 = "62652303"
TEST4 = "62655046"
TEST5 = "62660147"


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

    # Returns a list of URLs
    # Where we can pull all the fans associated with a specific set
    """Assumption that 200 results are stored on each page"""

    d = get_set_attributes(set_id)

    results = []

    for i in range(d['guess_fan_pages']):

        url_1 = "http://www.polyvore.com/cgi/set.fans?.in=json&.out=jsonx&request=%7B\"id\"%3A\""
        url_id = str(d['set_id'])
        url_2 = "\"%2C\"length\"%3A"
        url_length = str(200)
        url_3 = "%2C\"page\"%3A"
        url_pages = str(i + 1)  # Because Polyvore page count starts at 1
        url_4 = "%7D"

        guess_url = url_1 + url_id + url_2 + url_length + url_3 + url_pages + url_4
        
        results.append(guess_url)

    # Return list of URLs

    return results


def create_set_fan_files(set_id):

    ## Pull down the JSON files from Polyvore
    ## Write it to a text file
    ## Another method will parse through text file later

    polyvore_urls = get_set_fans_url(set_id)

    for i, url in enumerate(polyvore_urls):

        # Get the JSON string

        json_file = urllib.urlopen(url)
        json_string = json_file.read()
        json_dict = json.loads(json_string)

        # Save it to a text file

        target_filename = "json-files/set-fans-" + str(set_id) + "-p" + str(i+1) + ".txt"
        target_file = open(target_filename, 'w')
        target_file.write(json_string)
        target_file.close()


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

    """Convert these to the correct data type"""
    """**************************************"""
    """**************************************"""
    """**************************************"""

    # Pull basic set attributes from the JSON dict
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

    # Guess the number of pages we'll have to pull to get all the fans (for future reference, we'll use this number over and over)
    d['guess_fan_pages'] = guess_set_fan_pages(d['num_fans'])

    # Return a dictionary of set attributes
    return d


def guess_set_fan_pages(num_fans):

    ## Takes the number of fans associated with a given set
    ## Guesses the number of pages that these fans are stored on
    ## So you know how many URLs to pull
    ## Assume that Polyvore stores 200 results on each page

    fans = int(num_fans)
    guess_length = 200.0
    guess_pages = int(math.ceil(fans / guess_length))

    return guess_pages


def get_set_fans(set_id):

    ## Assumes that text files storing this data have already been created with create_set_fan_files()
    ## Returns a list of tuples with fan_id and fan_name
    ## ----- need fan_id because if it = 0 that means a user with no account
    ## ----- need fan_name because that is how each fan's page is accessed on Polyvore
    ## This list will be used to populate the Sets_Fans table, using a function in model.py

    fan_ids = []
    fan_names = []

    d = get_set_attributes(set_id)

    ## Iterate through the total number of pages, since fans for each set are stored on multiple pages
    for i in range(d['guess_fan_pages']):

        # Grab the JSON dictionary out of the text file
        target_filename = "json-files/set-fans-" + str(set_id) + "-p" + str(i+1) + ".txt"
        polyvore = get_json_dict(target_filename)

        # Iterate through all the fans stored on one page
        list_of_fans = polyvore["result"]["items"]

        for f in list_of_fans:
            fan_ids.append(f["object_id"])
            fan_names.append(f["user_name"])

    result = zip(fan_ids, fan_names)
    return result



















