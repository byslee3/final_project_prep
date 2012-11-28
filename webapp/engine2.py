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
        self.total_items = None
        self.percent_match = None

    def calculate_total_items(self):
        self.total_items = len(self.items_matching) + len(self.items_missing) + 0.0

    def calculate_percent_match(self):
        if not self.total_items:
            pass
        else:
            self.percent_match = round(len(self.items_matching) / self.total_items * 100, 1)


##############################################################################
######################### Inventory Selection ################################
##############################################################################


def connect_db():
    db = sqlite3.connect("polyvore.db")
    return db


# Testing purposes
db = connect_db()


# This works
def get_starting_items(db):

    """
    Return a list of dictionaries
    """

    # Get list of unique items
    query = """SELECT DISTINCT item_id FROM Test"""
    cursor = db.execute(query)
    unique_item_list = [  row[0] for row in cursor.fetchall()  ]

    # Select 5 of those items at random
    random_items = random.sample(unique_item_list, 5)

    # Store in a dictionary to pass to web interface
    # ---> Build this out later with additional attributes
    result = []

    for item_id in random_items:
        d = {}
        d["item_id"] = item_id
        result.append(d)

    return result


def get_next_items(db, this_round_selection, selected_inventory):

    """
    Return a list of dictionaries
    """

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

        # Store in a dictionary to pass to web interface
        # ---> Build this out later with additional attributes
        result = []

        for item_id in resulting_items:

            # Check first to see if it's already been selected
            if not item_id in selected_inventory:
                d = {}
                d["item_id"] = item_id
                result.append(d)

        return result


##############################################################################
##############################################################################
########################### Matching to Sets #################################
##############################################################################
##############################################################################

# Step 1a of the process
# Given the Items_Sets list, only pull out the records where item = in selected inventory
# ---> Need to index the Items_Sets table on item_id
def get_subset_matching_items(db, selected_inventory):

    """
    selected_inventory = a list of item_ids that the user selected
    result = returns a list of set_ids that contain those items
    will be called by another function
    """

    query_template = """SELECT * FROM Test WHERE item_id IN (%s)"""
    q_marks_string = ", ".join(["?"] * len(selected_inventory))
    query = query_template % q_marks_string

    cursor = db.execute(query, tuple(selected_inventory))
    result = [  row[2] for row in cursor.fetchall()  ]
    return result


# Step 1b of the process
# Now that we have all the sets + matching items, need to get all the sets + all items
def get_subset_all_items(db, selected_inventory):

    selected_sets = get_subset_matching_items(db, selected_inventory)

    query_template = """SELECT * FROM Test WHERE set_id IN (%s)"""
    q_marks_string = ", ".join(["?"] * len(selected_sets))
    query = query_template % q_marks_string
    cursor = db.execute(query, selected_sets)

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

        # If the set has not been recorded yet, create a new set object and store in dictionary
        if d.get(set_id) == None:

            d[set_id] = Set(set_id)

            # Determine whether the item is a matching or missing item, and update the Set object accordingly
            if item_id in selected_inventory:
                d[set_id].items_matching.append(item_id)
            else:
                d[set_id].items_missing.append(item_id)

        else:
            # Determine whether the item is a matching or missing item
            if item_id in selected_inventory:
                d[set_id].items_matching.append(item_id)
            else:
                d[set_id].items_missing.append(item_id)

    return d


# Step 3a of the process
# Calculate the percentage match of the sets
def calculate_percent_match(db, set_dictionary):

    for key, set_object in set_dictionary.iteritems():

        set_object.calculate_total_items()
        set_object.calculate_percent_match()

    return set_dictionary


# Step 3b of the process
# Return all of the sets that have a percent match above a certain cutoff
def return_sets_above_cutoff(db, set_dictionary, cutoff):

    d = {}

    for key, set_object in set_dictionary.iteritems():

        if set_object.percent_match >= cutoff:
            d[key] = set_object

    return d


# Final result that gets called by the web interface
def return_matching_sets(db, selected_inventory):

    """
    Returns a dictionary with each entry as:
    { set_id: set_object }
    """

    cutoff_percent = 50

    # Get subset of records for this analysis
    subset = get_subset_all_items(db, selected_inventory)

    # Aggregate into set dictionary
    set_dict = aggregate_into_sets(db, selected_inventory, subset)

    # Calculate the percentage match
    set_dict = calculate_percent_match(db, set_dict)

    # Return sets above the cutoff
    final_matching = return_sets_above_cutoff(db, set_dict, cutoff_percent)

    return final_matching


# For testing purposes
def print_set_dict(d):

    for key, obj in d.iteritems():
        print "****************************"
        print obj.items_matching
        print obj.items_missing
        print obj.total_items
        print obj.percent_match




##############################################################################
##############################################################################
########################### Return Updated Sets ##############################
##############################################################################
##############################################################################








def return_updated_sets(existing_sets, new_item):

    # Take the existing list of set objects
    # Take the new item and move it from the attribute:missing item >>> to the attribute:matching items
    # Recalculate the matching percentages

    # RETURN DUMMY DATA FOR NOW
    result = ["setA_obj", "setB_obj", "setC_obj", "setD_obj", "setE_obj"]
    return result
















