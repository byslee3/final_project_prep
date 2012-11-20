import json
import math
import urllib


SET1 = "62332524"
SET2 = "62652167"
SET3 = "62652303"
SET4 = "62655046"
SET5 = "62660147"

FAN1 = "3339312"
FAN2 = "3159094"
FAN3 = "1231532"

ITEM1 = "17109441"


#############################
####### JSON Requests #######
#############################


def create_filename(category, unique_id):

    if not category == "user":

        last_digit = unique_id[-1]

        # Use this for Item and Set
        filename = "json-files/%s/f%s/%s-%s.txt" %(category, last_digit, category, unique_id)
        return filename

    elif category == "user":

        # Dump them all in one folder for now since these are indexed by alphabetical usernames

        filename = "json-files/user/user-%s.txt" %(unique_id)
        return filename


def create_filename_paged(category, unique_id, page):

    last_digit = unique_id[-1]

    # Use this for Set-Fan, User-Item, User-Set
    # Results for one object are stored on multiple pages
    filename = "json-files/%s/f%s/%s-%s-p%s.txt" %(category, last_digit, category, unique_id, page)
    return filename


def get_set_url(set_id, seo_title):

    # Get the URL for any Polyvore set
    # Will be called by another method that writes the JSON string to a text file

    url_1 = "http://www.polyvore.com/"
    url_2 = "/set?id="
    url_3 = "&.out=json"

    target_url = url_1 + seo_title + url_2 + str(set_id) + url_3

    return target_url


def create_set_file(set_id, seo_title):

    try:
        # Grabs the JSON string for any Polyvore set, given the set_id and seo_title  
        set_url = get_set_url(set_id, seo_title)
        json_file = urllib.urlopen(set_url)
        json_string = json_file.read()
        json_file.close()

        # Create a file named after the set and write the JSON string to it
        target_filename = create_filename("set", set_id)
        target_file = open(target_filename, 'w')
        target_file.write(json_string)
        target_file.close()

    except UnicodeError:
        pass


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

        try:
            # Get the JSON string
            json_file = urllib.urlopen(url)
            json_string = json_file.read()
            json_dict = json.loads(json_string)
            json_file.close()

            # Save it to a text file
            target_filename = create_filename_paged("set-fan", set_id, str(i+1))
            target_file = open(target_filename, 'w')
            target_file.write(json_string)
            target_file.close()

        except UnicodeError:
            pass


def get_user_url(user_name):

    # Get the JSON location for any Polyvore user

    url_1 = "http://"
    url_2 = ".polyvore.com/?.out=json"

    target_url = url_1 + user_name + url_2
    return target_url


def create_user_file(user_name):

    try:
        # Grabs the JSON string for any Polyvore user, given their user name
        user_url = get_user_url(user_name)
        json_file = urllib.urlopen(user_url)
        json_string = json_file.read()
        json_file.close()

        # Create a file named after the user and write the JSON string to it
        target_filename = create_filename("user", user_name)
        target_file = open(target_filename, 'w')
        target_file.write(json_string)
        target_file.close()

    except UnicodeError:
        pass



def get_item_url(item_id, item_seo_title):

    # Get the JSON location for any Polyvore item

    url_1 = "http://www.polyvore.com/"
    url_2 = "/thing?id="
    url_3 = "&.out=json"

    target_url = url_1 + item_seo_title + url_2 + str(item_id) + url_3
    return target_url


def create_item_file(item_id, item_seo_title):

    try:
        # Grabs the JSON string for any Polyvore user, given their user name
        item_url = get_item_url(item_id, item_seo_title)
        json_file = urllib.urlopen(item_url)
        json_string = json_file.read()
        json_file.close()

        # Create a file named after the user and write the JSON string to it
        target_filename = create_filename("item", item_id)
        target_file = open(target_filename, 'w')
        target_file.write(json_string)
        target_file.close()

    except UnicodeError:
        pass


def get_user_sets_url(user_id):

    # Returns a list of URLs where you can get the sets that a user Liked
    # Each page has 25 sets. Pull 50 sets that the user Liked.
    # Pull 2 pages. If the user has less than 2 pages, it will pull the last page multiple times.

    url_1 = "http://www.polyvore.com/cgi/browse.likes?filter=sets&page="
    url_2 = "&uid="
    url_3 = "&.out=json"

    target_urls = []

    for i in range(1,3):

        target_url = url_1 + str(i) + url_2 + str(user_id) + url_3
        target_urls.append(target_url)

    return target_urls


def get_user_items_url(user_id):

    # Returns a list of URLs where you can get the items that a user Liked
    # Each page has 25 items. Pull 100 items that the user Liked.
    # Pull 4 pages. If the user has less than 4 pages, it will pull the last page multiple times.

    url_1 = "http://www.polyvore.com/cgi/browse.things?page="
    url_2 = "&uid="
    url_3 = "&.out=json"

    target_urls = []

    for i in range(1,5):

        target_url = url_1 + str(i) + url_2 + str(user_id) + url_3
        target_urls.append(target_url)

    return target_urls


def create_user_sets_files(user_id):

    ## Pull down the JSON files from Polyvore
    ## Write it to a text file. Another method will parse through text file later.
    polyvore_urls = get_user_sets_url(user_id)

    for i, url in enumerate(polyvore_urls):

        try:
            # Get the JSON string
            json_file = urllib.urlopen(url)
            json_string = json_file.read()
            json_dict = json.loads(json_string)
            json_file.close()

            # Save it to a text file
            target_filename = create_filename_paged("user-set", user_id, str(i+1))
            target_file = open(target_filename, 'w')
            target_file.write(json_string)
            target_file.close()

        except UnicodeError:
            pass


def create_user_items_files(user_id):

    ## Pull down the JSON files from Polyvore
    ## Write it to a text file. Another method will parse through text file later.
    polyvore_urls = get_user_items_url(user_id)

    for i, url in enumerate(polyvore_urls):

        try:
            # Get the JSON string
            json_file = urllib.urlopen(url)
            json_string = json_file.read()
            json_dict = json.loads(json_string)
            json_file.close()

            # Save it to a text file
            target_filename = create_filename_paged("user-item", user_id, str(i+1))
            target_file = open(target_filename, 'w')
            target_file.write(json_string)
            target_file.close()

        except UnicodeError:
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


def get_item_attributes(item_id):

    # Returns the item attributes as a dictionary
    d = {}

    # Open the appropriate JSON file and read from it
    filename = create_filename("item", item_id)
    polyvore = get_json_dict(filename)

    """Convert these to the correct data type"""
    """**************************************"""
    """**************************************"""
    """**************************************"""

    # Pull basic item attributes from the JSON dict
    d['item_id'] = polyvore["thing"]["thing_id"]
    d['seo_title'] = polyvore["thing"]["seo_title"]
    d['title'] = polyvore["thing"]["title"]
    d['age'] = polyvore["thing"]["age"]
    d['imgurl'] = polyvore["thing"]["imgurl"]
    d['save_count'] = polyvore["thing"]["save_count"]
    d['category_id'] = polyvore["thing"]["category_id"]
    d['brand_id'] = polyvore["thing"]["brand_id"]
    d['brand_name'] = polyvore["thing"]["brand"]
    d['usd_price'] = polyvore["thing"].get("usd_price", -1)   # Getting a key error when we try to pull usd_price --> It's because some items have prices(thus are a product) but don't have a USD price. Argh!

    # This may or may not exist for all objects (?)
    if polyvore["thing"].get("shop_link"):
        d['anchor'] = polyvore["thing"]["shop_link"].get("anchor", None)
    else:
        d['anchor'] = None

    # More basic stuff that only exists if this is a sponsored item
    if polyvore.get("thing_sponsored"):
        d['retailer'] = polyvore["thing_sponsored"]["targeting"]["retailer"]
        # d['tags_sponsored'] = polyvore["thing_sponsored"]["targeting"]["cat"]
    else:
        d['retailer'] = "0"
    
    # Each item also has tags, but these will have to be pulled separately and stored in an Item-Tag linkage table. Many to many relationship.
    # d['tags'] = polyvore["thing"]["tags"]   

    return d

def get_user_attributes(user_name):

    # Returns the item attributes as a dictionary
    d = {}

    # Open the appropriate JSON file and read from it
    filename = "json-files/user/user-" + str(user_name) + ".txt"  # Can't use % method because some usernames have numbers in them
    polyvore = get_json_dict(filename)

    """Convert these to the correct data type"""
    """**************************************"""
    """**************************************"""
    """**************************************"""

    # Basic stuff
    d['user_id'] = polyvore["user"]["user_id"]
    d['user_name'] = polyvore["user"]["user_name"]
    d['country'] = polyvore["user"]["country"]
    d['createdon_ts'] = polyvore["user"]["createdon_ts"]

    return d


def get_set_attributes(set_id):

    # Returns the set attributes as a dictionary
    d = {}

    # Open the appropriate JSON file and read from it
    filename = create_filename("set", set_id)
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
    # ----- Pull only the basic attributes that will be put into the Sets table
    # ----- Do not pull many-to-many relationships as those will be put in separate linkage tables
    # ----- Those will be pulled in separate functions

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



def get_set_items(set_id):

    ## This information is located directly in the JSON for each specific set
    ## Returns a list of tuples with item_ids and item_seo_titles (need both for accessing Polyvore page)
    ## This list will be used to populate the Sets_Items table, using a function in model.py

    ## ----- Limitation:
    ## ----- We only pull the items that are denoted as products by polyvore["overlay_items"][i]["is_product"] == 1
    ## ----- This differentiates between background graphics and clothing/fashion products
    ## ----- HOWEVER, some products are not tagged as products, because they are not available for sale online
    ## ----- Our model/database will miss these products (but spot checking shows that all main relevant products are captured)

    item_ids = []
    item_seo_titles = []

    # Open the appropriate JSON file and read from it
    filename = create_filename("set", set_id)
    polyvore = get_json_dict(filename)

    # Iterate through all the items in the set
    for item in polyvore["overlay_items"]:

        # Check if it's a product or a graphic
        if item.get("is_product",0) == 1:

            item_id = item["thing_id"]
            item_seo_title = item["seo_title"]

            # Check for duplicates
            if not item_id in item_ids:
                item_ids.append(item_id)
                item_seo_titles.append(item_seo_title)

    result = zip(item_ids, item_seo_titles)
    return result


def get_user_sets(user_id):

    ## Assumes that text files storing this data have already been created with create_set_fan_files()
    ## Returns a list of tuples with set_id and set_seo_title
    ## Need both of these to get the Polyvore URL for a set
    ## This list will be used to "reverse" populate the Sets_Fans table, using a function in model.py

    set_ids = []
    set_seo_titles = []

    ## Iterate through 2 total pages. Each page stores 25 sets.
    for i in range(1,3):

        # Grab the JSON dictionary out of the text file
        target_filename = create_filename_paged("user-set", user_id, str(i))
        polyvore = get_json_dict(target_filename)

        # Iterate through all the sets stored on one page
        for set in polyvore["result"]["items"]:
            set_id = set["id"]
            set_seo_title = set["seo_title"]

            # Check for duplicates (in case last page pulled more than once)
            if not set_id in set_ids:
                set_ids.append(set_id)
                set_seo_titles.append(set_seo_title)

    result = zip(set_ids, set_seo_titles)
    return result


def get_user_items(user_id):

    ## Assumes that text files storing this data have already been created with create_set_fan_files()
    ## Returns a list of tuples with item_id and item_seo_title
    ## Need both of these to get the Polyvore URL for a set

    item_ids = []
    item_seo_titles = []

    ## Iterate through 4 total pages. Each page stores 25 sets.
    for i in range(1,5):

        # Grab the JSON dictionary out of the text file
        target_filename = create_filename_paged("user-item", user_id, str(i))
        polyvore = get_json_dict(target_filename)

        # Iterate through all the items stored on one page
        for item in polyvore["result"]["items"]:

            # Check if it's a product (using existence of price tag as a proxy)
            if item.get("price",-1) > 0:

                item_id = item["thing_id"]
                item_seo_title = item["seo_title"]

                # Check for duplicates (in case last page pulled more than once)
                if not item_id in item_ids:

                    item_ids.append(item_id)
                    item_seo_titles.append(item_seo_title)

    result = zip(item_ids, item_seo_titles)
    return result


def get_item_sets(item_id):

    ## For a given item, returns all the sets that it is associated with
    ## Returns a list of tuples with set_id and set_seo_title
    ## This list will be used to "reverse" populate the Sets_Items table (stored as a separate Items_Sets table for now)
    ## ---> New edit Nov 20: Return clickurl and imgurl as well in this table, instead of pulling all the set ids and then pulling from there (b/c there will be approx 1M and takes too long to pull)

    set_ids = []
    set_seo_titles = []
    imgurls = []

    # Open the appropriate JSON file and read from it
    filename = create_filename("item", item_id)
    polyvore = get_json_dict(filename)

    # Iterate through all the collections associated with this item
    for collection in polyvore["collections"]:

        # Check that it's a set and not a collection
        # Wanted to check if it's a fashion set, but that info is not included here
        if collection.get("object_class", "999") == "set":

            set_id = collection["id"]
            set_seo_title = collection["seo_title"]
            imgurl = collection["imgurl"]

            set_ids.append(set_id)
            set_seo_titles.append(set_seo_title)
            imgurls.append(imgurl)

    result = zip(set_ids, set_seo_titles, imgurls)
    return result















