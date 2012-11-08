import json
import urllib
import math


########## Currently pulling the JSON manually and storing it in text files
########## In the future, use my_url = urllib.urlopen("http://www....")

"""
Page for a specific set
http://www.polyvore.com/blue_cream/set?id=62669278&.out=json
json_set_page.txt

Page for a specific item
http://www.polyvore.com/giambattista_valli_nappa_lace-up_boot/thing?id=58915848&.out=json
json_item_page.txt

Page for a specific user (fan)
http://iiina.polyvore.com/?.out=json
json_user_fan_page.txt

Page for a specific user (set creator)
http://drn57.polyvore.com/?.out=json
json_user_creator_page.txt
^^^^^ This is the same as a page for a fanvbv 

Page (from the shopping section) with a lot of items on it (try to cross reference?)
http://www.polyvore.com/cgi/shop?brand=Giambattista+Valli&category_id=41&query=&.out=json
json_shopping_page.txt
^^^^^ This one is not useful for our purposes. We can get the category tags from item page instead.

Page (linked to the specific set) that holds all of the fans
URL is determined by print_data_set function for the sample set that we picked
json_set_all_fans_1.txt
json_set_all_fans_2.txt
json_set_all_fans_3.txt

"""

########## Dictionary for commands and filenames
file_list = [
    "json_set_page.txt",
    "json_item_page.txt",
    "json_user_fan_page.txt",
    "json_user_creator_page.txt",
    "json_shopping_page.txt"
]

########## Get the JSON and format it
def get_JSON_dict(filename):
    f = open(filename)
    json_string = f.read()
    json_dict = json.loads(json_string)
    f.close()

    return json_dict

########## Print the entire dict, formatted
def print_formatted_JSON(json_dict):
    print json.dumps(json_dict, indent=4)

########## Print the keys
def print_keys(json_dict):
    list_of_keys = json_dict.keys()

    for k in list_of_keys:
        print k

########## Command prompt
def run_commands():

    # List of files to pick from
    global file_list
    for i in range(0,len(file_list)):
        print str(i) + " ------> " + file_list[i]

    entered_index = int(raw_input("Which file do you want to open? "))
    file_to_open = file_list[entered_index]

    #Print the keys first, then JSON string
    for i in range(0,10):
        print "+"

    print_keys(get_JSON_dict(file_to_open))

    for i in range(0,10):
        print "+"

    print_formatted_JSON(get_JSON_dict(file_to_open))

#########################################################
#########################################################
#########################################################

def print_data_set():

    filename = file_list[0]
    polyvore = get_JSON_dict(filename)

    d = {}

    d['test'] = "test value"

    # Basic stuff about the set
    d['set_id'] = polyvore["collection"]["id"]
    d['anchor'] = polyvore["collection"]["embed_anchor"]["anchor"]
    d['pageviews'] = polyvore["collection"]["pageview"]
    d['title'] = polyvore["collection"]["title"]
    d['createdon'] = polyvore["collection"]["createdon"]
    d['score'] = polyvore["collection"]["score"]
    d['confirmed_tags'] = polyvore["confirmed_tags"]

    # Grabbing all the items in the set
    d['num_set_items_all'] = len(polyvore["overlay_items"])

    d['set_items'] = []
    d['set_items_names'] = []

    for i in range(d['num_set_items_all']):

        if polyvore["overlay_items"][i].get("is_product",0) == 1:

            item_id = polyvore["overlay_items"][i]["thing_id"]
            item_name = polyvore["overlay_items"][i]["title"]

            d['set_items'].append(item_id)
            d['set_items_names'].append(item_name)

    d['num_set_items_valid'] = len(d['set_items'])
    
    # Info about the creator
    d['creator_id'] = polyvore["collection"]["user_id"]
    d['creator_name'] = polyvore["collection"]["user_name"]

    # Need to pull the fan ids
    # But first need to get all the fan ids onto one page
    d['num_fans'] = polyvore["fav_count"]
    d['guess_fan_json'] = []

    fans = int(polyvore["fav_count"])
    fans = 563  # ------------------ hard code this for now for this example
    guess_length = 200.0
    guess_pages = int(math.ceil(fans / guess_length))

    # ------- Guess the URLs that the fans are stored on
    for i in range(guess_pages):

        url_1 = "http://www.polyvore.com/cgi/set.fans?.in=json&.out=jsonx&request=%7B\"id\"%3A\""
        url_id = str(d['set_id'])
        url_2 = "\"%2C\"length\"%3A"
        url_length = str(int(guess_length))
        url_3 = "%2C\"page\"%3A"
        url_pages = str(i + 1)  # Because Polyvore page count starts at 1
        url_4 = "%7D"

        guess_url = url_1 + url_id + url_2 + url_length + url_3 + url_pages + url_4
        
        d['guess_fan_json'].append(guess_url)

    # ------- Store the fan results into text files
    # ------- Need to write this part

    # ------- Loop through text files and pull fan ids from the text files

    d['fan_ids'] = []

    for i in range(guess_pages):
        filename = "json_set_all_fans_" + str(i + 1) + ".txt" # -------- Will need to modify this later to include set id in file name
        additional_fans = get_all_fans(filename)
        d['fan_ids'].extend(additional_fans)

    d['num_fan_ids'] = len(d['fan_ids']) # ------- This is just a check for now

    # Print out all the data at the end
    for key, value in d.iteritems():
        print "................."
        print key
        print value


def get_all_fans(filename):

    # Assume that we've used a separate function to pull all the JSON strings
    # and store them in text files
    
    polyvore = get_JSON_dict(filename)

    list_of_fans = polyvore["result"]["items"]
    fan_ids = []
    fan_names = []

    for f in list_of_fans:
        fan_ids.append(f["object_id"])
        fan_names.append(f["user_name"])

    return fan_ids




