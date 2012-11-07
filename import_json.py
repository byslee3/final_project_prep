import json
import urllib

#my_url = urllib.urlopen("http://www.polyvore.com/sin_t%C3%ADtulo_892/set?id=62332524&.out=json")
#I've stored the equivalent in json_output.txt
#This URL corresponds to the page for a specific set

########## Get the JSON and format it
f = open("json_output.txt")
json_string = f.read()
json_dict = json.loads(json_string)
f.close()

########## Print the keys and how many things associated with them
list_of_keys = json_dict.keys()

for k in list_of_keys:
    print k

########## Print the entire dict, formatted
print json.dumps(json_dict, indent=4)