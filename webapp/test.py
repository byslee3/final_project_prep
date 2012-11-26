import sqlite3
import random


def get_starting_items(db):
    test = ["aaa", "bbb", "ccc", "ddd", "eee"]
    return test

def get_next_items(db, this_round_selection):
    test = ["AAA", "BBB", "CCC", "DDD", "EEE"]
    return test





def main():

    #db = sqlite3.connect("polyvore.db")
    db = "test"

    selected_inventory = []

    display_list = get_starting_items(db)  # First time through: Get 5 random seed items

    while len(selected_inventory) < 100:   # Ultimately may turn out slightly longer than 100 if they select multiple items on last time through loop

        # Print out the options
        command_num = 1

        for item in display_list:
            print str(command_num) + " ---> " + item

        # Get input from user
        # Need to loop through until they've entered everything
        answer = -1
        this_round_selection = []

        while answer != 0:
            
            answer = raw_input("Add item or '0' to submit marked items: ")

            if answer != 0:
                selected_item = display_list[answer - 1]
                selected_inventory.append(selected_item)
                this_round_selection.append(selected_item)

        # Once user has submitted their selections, get the next round of items to show them
        display_list = get_next_items(db, this_round_selection)

    print selected_inventory






##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################




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
# subset = get_subset_based_on_items(db, selected_inventory)


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


# Get the sets that have 4 or 5 items in them
def print_target_sets(db):

    #global db

    query = """SELECT set_id, COUNT(item_id) FROM Items_Sets GROUP BY set_id"""
    cursor = db.execute(query)

    result = [  row for row in cursor.fetchall()  ]

    #db.close()

    return result

# Delete anything that isn't in the target sets (this is a test database for now)
# Full database is stored in another file
def delete_non_targets():

    global db
    reference_list = print_target_sets(db)

    test = 0

    for tup in reference_list:

        if tup[1] < 4:   # Then delete from database for now
            query = """DELETE FROM Items_Sets WHERE set_id = ?"""
            cursor = db.execute(query, (tup[0],))
            print str(test) + " ----> item deleted"

        elif tup[1] >= 4:   # Then do nothing and keep it in the database
            print str(test)

        test += 1


    db.close()
















