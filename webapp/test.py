import sqlite3
import random


# For testing purposes
selected_inventory_test = [
'57295956', '67870971', '67861593', '14428033',
'24719080', '29485094', '43783147', '58034310',
'9275563', '69635837', '64527026', '62855670',
'9497001', '7556411', '67870785', '66786539',
'66866385', '66032594', '69920782', '65283476',
'67309090']


##############################################################################
########################### Class Definition #################################
##############################################################################

class Set(object):

    def __init__(self, set_id):
        self.set_id = set_id
        self.items_matching = []
        self.items_missing = []
        self.items_all = []
        self.match_percentage = None

    def update_items_matching(item_id):
        self.items_matching.append(item_id)



















##############################################################################
######################### Inventory Selection ################################
##############################################################################



def connect_db():
    db = sqlite3.connect("polyvore.db")
    return db


# This works
def get_starting_items(db):

    # Get list of unique items
    query = """SELECT DISTINCT item_id FROM Test"""
    cursor = db.execute(query)
    unique_item_list = [  row[0] for row in cursor.fetchall()  ]

    # Select 5 of those items at random
    random_items = random.sample(unique_item_list, 5)
    return random_items


def get_next_items(db, this_round_selection):

    # If this_round_selection is blank, i.e. user selected only dups
    # Just return a new round of random items
    if not this_round_selection:
        return get_starting_items(db)

    else:

        # Given a list of items: this_round_selection
        # Get a list of the records that contain those items. Get the set_ids from that.
        query_template = """SELECT DISTINCT set_id FROM Test WHERE item_id IN (%s)"""
        q_marks_string = ", ".join(["?"] * len(this_round_selection))
        query = query_template % q_marks_string
        
        cursor = db.execute(query, tuple(this_round_selection))
        resulting_sets = [  row[0] for row in cursor.fetchall()  ]

        # Get all of the records with those set_ids. Pull the distinct item_ids that are associated.
        # Return those item_ids
        query_template_2 = """SELECT DISTINCT item_id FROM Test WHERE set_id IN (%s)"""
        q_marks_string_2 = ", ".join(["?"] * len(resulting_sets))
        query_2 = query_template_2 % q_marks_string_2

        cursor_2 = db.execute(query_2, tuple(resulting_sets))
        resulting_items = [  row[0] for row in cursor_2.fetchall()  ]

        return resulting_items


## This contains a working command structure for having the user select inventory
def main():

    db = sqlite3.connect("polyvore.db")

    selected_inventory = []

    display_list = get_starting_items(db)  # First time through: Get 5 random seed items

    # Should be 100 but set to 20 for testing for now
    # Ultimately may turn out slightly longer than 100 if they select multiple items on last time through loop
    while len(selected_inventory) < 20:

        # Print out the options
        command_num = 1

        for item in display_list:
            print str(command_num) + " ---> " + item
            command_num += 1

        # Get input from user
        # Need to loop through until they've entered everything
        num = raw_input("Enter selected items -- separate them by a space: ")
        list_of_nums = num.strip().split(" ")

        this_round_selection = []
        
        for num in list_of_nums:
            selected_item = display_list[int(num) - 1]

            if not selected_item in selected_inventory:  # Prevent duplicates
                selected_inventory.append(selected_item)
                this_round_selection.append(selected_item)

        # Once user has submitted their selections, get the next round of items to show them
        display_list = get_next_items(db, this_round_selection)

    print selected_inventory


##############################################################################
########################### Matching to Sets #################################
##############################################################################

# Step 1 of the process
# Given the Items_Sets list, only pull out the records where item = in selected inventory
# ---> Need to index the Items_Sets table on item_id
def get_subset_based_on_items(db, selected_inventory):

    query_template = """SELECT * FROM Test WHERE item_id IN (%s)"""
    q_marks_string = ", ".join(["?"] * len(selected_inventory))
    query = query_template % q_marks_string

    cursor = db.execute(query, tuple(selected_inventory))
    result = [  row for row in cursor.fetchall()  ]
    return result


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

    """Returns this dictionary: but it only includes matching items"""
    """Need to go back through and get the rest of the items"""



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











