import sqlite3
import random

# This will get information out of the database and feed it into recommender.py
# For now (database is loading) send over dummy data and fill in functions later


#####
##### -----> NEED TO WRITE THIS
# Need to write class definition for a set object
# Attribute 1: list of matching objects to inventory
# Attribute 2: list of all objects in set
# Attribute 3: (derived) percentage of matching objects
# Attribute 4: (derived) still missing objects --> can use this to surface suggested items
#####
#####


# Global variables to store the num of records in each table (faster than having to do select count each time)
# Keep this updated as the database changes
NUM_ITEMS = 41812

## This is just for testing purposes. (will be passed from recommender.py later)
db = sqlite3.connect("polyvore.db")
selected_inventory = [
"57049384",
"59412350",
"64965861",
"66943923",
"68480485",
"68078611",
"64495413",
"65106361",
"24433814",
"67836525"]



####################################
########### Functions ##############
####################################


def get_starting_items(db):

    """
    Return a list of dictionaries
    That represents 100 items to be displayed in starting inventory
    Right now: select them randomly. Future ---> Refine
    """

    # Right now, pick the numbers randomly ---> Refine later
    global NUM_ITEMS
    random_ids = tuple(random.sample(xrange(1,NUM_ITEMS+1), 100))

    # SQL query
    query_template = """SELECT * FROM Items WHERE id IN (%s)"""
    q_marks_string = ", ".join(["?"] * 100)
    query = query_template % q_marks_string
    cursor = db.execute(query, random_ids)

    # Store the results of query
    result = []

    for row in cursor.fetchall():
        d = {}
        d["item_id"] = row[1] 
        d["imgurl"] = row[6]
        d["title"] = row[3]
        result.append(d)

    return result



def return_matching_sets(db, selected_inventory):

    print selected_inventory



    # Takes a list of items that the user has selected as being in the inventory
    # Goes through all the sets in the database and finds the matching ones

    # -----> To make it run quickly for now, only go through first 5,000 sets

    # -----> This is going to need to call a bunch of sub-functions (see diagram in notebook)
    # -----> Rank the sets by % match, or have a cutoff (put this in sub-function)

    # RETURN DUMMY DATA FOR NOW
    # Ultimately return a list of set objects that contains lots of different data that I need
    # (so that we don't have to call this function over and over)
    result = selected_inventory
    return result


def return_updated_sets(existing_sets, new_item):

    # Take the existing list of set objects
    # Take the new item and move it from the attribute:missing item >>> to the attribute:matching items
    # Recalculate the matching percentages

    # RETURN DUMMY DATA FOR NOW
    result = ["setA_obj", "setB_obj", "setC_obj", "setD_obj", "setE_obj"]
    return result


# Step 1 of the process
# Given the Items_Sets list, only pull out the records where item = in selected inventory
# ---> Need to index the Items_Sets table on item_id
def get_subset_based_on_items(db, selected_inventory):

    query_template = """SELECT * FROM Items_Sets WHERE item_id IN (%s)"""
    q_marks_string = ", ".join(["?"] * len(selected_inventory))
    query = query_template % q_marks_string

    cursor = db.execute(query, tuple(selected_inventory))

    result = [  row for row in cursor.fetchall()  ]
    return result


# For testing --> delete later
subset = get_subset_based_on_items(db, selected_inventory)


# Step 2 of the process
# Now that we have the subset, group the items into the sets
def aggregate_into_sets(db, selected_inventory, subset):

    """
    selected_inventory = a list of item_ids
    subset = subset of records from Items_Sets
    """

    d = {}

    for record in subset:

        item_id = record[1]
        set_id = record[2]

        if d.get(set_id) == None:   # Means the set has not been recorded yet
            d[set_id] = [item_id]   # Create a new list and store this item as the first entry
        else:                           # Else
            d[set_id].append(item_id)   # Add this item_id to the existing entry

    for key, value in d.iteritems():
        print "+++++++++++++++++"
        print key
        print value


####################################
########### Debugging ##############
####################################

def print_set_histogram():

    # SQL query
    global db

    query = """SELECT set_id, COUNT(item_id) FROM Items_Sets GROUP BY set_id"""
    cursor = db.execute(query)

    result = [  row for row in cursor.fetchall()  ]

    db.close()

    # Building the histogram
    histogram = {"1":0, "2":0, "3":0, "4":0, "5":0}

    for tup in result:

        num_items = tup[1]

        if num_items <= 4:
            histogram[str(num_items)] += 1
        elif num_items > 4:
            histogram["5"] += 1

    # Print histogram

    for key, value in histogram.iteritems():
        print "Number of sets that contain %s item(s): %d" % (key, value)

    print histogram















