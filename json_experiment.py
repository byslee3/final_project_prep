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

Page (from the shopping section) with a lot of items on it (try to cross reference?)
http://www.polyvore.com/cgi/shop?brand=Giambattista+Valli&category_id=41&query=&.out=json
json_shopping_page.txt

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
def get_JSON_string(filename):
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

########## Pick which file to open
def main():

    global file_list
    for i in range(0,len(file_list)):
        print str(i) + " ------> " + file_list[i]

    entered_index = int(raw_input("Which file do you want to open? "))
    file_to_open = file_list[entered_index]

    print_formatted_JSON(get_JSON_string(file_to_open))

main()