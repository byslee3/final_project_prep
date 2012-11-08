import json
import urllib


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

    # Basic stuff
    d ['set_id'] = polyvore["collection"]["id"]
        # See what else you can pull from the "collection" field

    # Grabbing all the items in the set
    d['num_set_items'] = len(polyvore["overlay_items"])
    d['set_items'] = []
    for i in range(d['num_set_items']):
        item_id = polyvore["overlay_items"][i]['thing_id']
        d['set_items'].append(item_id)
        # Should this be pulled from the "collection" field instead?
    

    # Need to pull the fan ids
    # But first need to get all the fan ids onto one page
    d['num_fans'] = polyvore["fav_count"]


    # Print out all the data at the end
    for key, value in d.iteritems():
        print "................."
        print key
        print value






