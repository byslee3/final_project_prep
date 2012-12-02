import sqlite3
import random


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


class Item(object):

    def __init__(self, item_id):
        self.item_id = item_id
        self.imgurl = None

##############################################################################
######################### Inventory Selection ################################
##############################################################################


def connect_db():
    db = sqlite3.connect("polyvore.db")
    return db


def get_random_items(db, num_to_get, items_already_selected=[]):
    """
    Pull X items at random from database
    Make sure they're not items you already pulled
    num_to_get needs to be at least 1
    items_already_selected is a list of item_ids
    Return a list of item objects
    """

    # Get list of unique items
    # Modify the query so that it DOESN'T select any items that have already been selected
    """ NEED TO FIX THIS PART LATER """
    query = """SELECT DISTINCT item_id FROM Test"""
    cursor = db.execute(query)
    unique_item_list = [  row[0] for row in cursor.fetchall()  ]

    # Select X of those items at random
    result = []
    random_items = random.sample(unique_item_list, num_to_get)

    for item_id in random_items:
        item = Item(item_id)
        result.append(item)

    return result


def test1():

    db = connect_db()

    # This one should return any number in test version where unique_item_list = ["333", "222", "555", "111"] (won't work after I update the function)
    # answer = get_random_items(db, 1)

    # This one should return only ["111"]
    #answer = get_random_items(db, 1, ["333", "222", "555"])

    # This one should return any 2 items
    answer = get_random_items(db, 5)

    print answer

    print "*******"

    for item_obj in answer:
        print item_obj.item_id



def format_list(db, item_list):

    """
    Format a list of item objects into groups of 4
    Needed for the grid structure of the html layout
    Takes item_list = [obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8]
    Returns a list of item objects in this format: list = [[obj1, obj2, obj3, obj4], [obj5, obj6 obj7, obj8]]
    If the item_list is not a multiple of 4, this function will pull extra random items to make up the difference
    """

    # See if we need to get additional items
    remainder = len(item_list) % 4

    if remainder > 0 or len(item_list)==0:
        num_to_get = 4 - remainder
        addition = get_random_items(db, num_to_get)
        item_list.extend(addition)

    # Now that the list is a multiple of 4, group it into the appropriate format
    num_groups = len(item_list) / 4

    formatted_list = []

    for num in range(0, num_groups):
        group = [None, None, None, None]
        group[0] = item_list[0 + num*4]
        group[1] = item_list[1 + num*4]
        group[2] = item_list[2 + num*4]
        group[3] = item_list[3 + num*4]
        formatted_list.append(group)

    return formatted_list

# Unit test for format_list function. It works!
def test2():
    db = connect_db()

    list1 = [1, 2, 3, 4, 5, 6, 7, 8]
    format_list(db, list1)

    print "***********************"

    list2 = [1, 2, 3, 4, 5, 6, 7]
    format_list(db, list2)

    print "***********************"

    list3 = [1, 2, 3, 4, 5]
    format_list(db, list3)

    print "***********************"

    list4 = [1, 2, 3, 4]
    format_list(db, list4)

    print "**********************"

    list5 = [1, 2, 3]
    format_list(db, list5)

    print "**********************"

    list6 = [1]
    format_list(db, list6)

    print "**********************"

    list7 = []
    format_list(db, list7)

# This works
def get_starting_items(db):

    """
    Return a list of item objects
    """

    # Get list of unique items
    query = """SELECT DISTINCT item_id FROM Test"""
    cursor = db.execute(query)
    unique_item_list = [  row[0] for row in cursor.fetchall()  ]

    # Select 8 of those items at random (to fit with grid structure of html layout)
    random_items = random.sample(unique_item_list, 8)

    # Create list of Item objects
    # ---> Build this out later with additional attributes
    result = []

    for item_id in random_items:
        item = Item(item_id)
        result.append(item)

    formatted_result = format_list(db, result)

    return formatted_result


def get_next_items(db, this_round_selection, selected_inventory):

    """
    Return a list of item objects
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

        # List of item objects
        # ---> Build this out later with additional attributes
        result = []

        for item_id in resulting_items:

            # Check first to see if it's already been selected
            if not item_id in selected_inventory:
                item_object = Item(item_id)
                result.append(item_object)

        formatted_result = format_list(db, result)

        return formatted_result


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
    selected_inventory = a list of item_ids
    result = returns a list of set_ids that contain those items
    will be called by another function
    """

    # Database query
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
def return_sets_above_cutoff(set_dictionary, cutoff):

    d = {}

    for key, set_object in set_dictionary.iteritems():

        if set_object.percent_match >= cutoff:
            d[key] = set_object

    return d


# Step X: Get all of the potential matching sets, not just the ones above cutoff
# We'll need this later for getting the suggested items
def all_potential_sets(db, selected_inventory):

    """
    Returns a dictionary with each entry as:
    { set_id: set_object }
    """

    # Get subset of records for this analysis
    subset = get_subset_all_items(db, selected_inventory)

    # Aggregate into set dictionary
    set_dict = aggregate_into_sets(db, selected_inventory, subset)

    # Calculate the percentage match
    set_dict = calculate_percent_match(db, set_dict)

    return set_dict


# Final result that gets called by the web interface
# Pass it Step X to get here, since we'll need Step X elsewhere in recommender.py
def return_matching_sets(db, all_potential_sets):

    """
    Returns a dictionary with each entry as:
    { set_id: set_object }
    """

    cutoff_percent = 50

    # Return sets above the cutoff
    final_matching = return_sets_above_cutoff(all_potential_sets, cutoff_percent)

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


def get_suggested_items(all_potential_sets):

    """
    Need to get the set_dictionary BEFORE we only get the ones with the cutoffs
    Pass in a dictionary of {set_id: set_object}
    Return a list of item_ids
    ---> Later, should refine this method
    """

    result = []

    for key, set_object in all_potential_sets.iteritems():
        result.extend(set_object.items_missing)

    # Create a table out of all the results
    #   column 1 = item_id
    #   column 2 = the set to which it belongs, what is the percent? how far away from the cutoff is it?
    # Create another table out of this
    #   column 1 = item_id
    #   column 2 = how many times does this item_id occur? i.e. does this item_id push multiple sets over the cutoff?

    # pick 8 or 16 items to continue

    return result




def return_updated_sets(all_potential_sets, list_of_new_items):

    """
    Pass in a dictionary of {set_id: set_object}. Usually this will be the currently matching sets
    Pass in an item_id for a potential new item
    Take the new item and move it from set_object.items_missing ---> set_object.items_matching
    (need to use a roundabout way because you can't modify the list at the same time you are iterating through it)
    (list references are weird)
    Recalculate the matching percentages
    Returns a dictionary of format {set_id: set_object}
    ---> It feels like the runtime for this could be very long
    """

    for key, set_object in all_potential_sets.iteritems():

        move_these_items = []
        keep_these_in_missing = []

        for missing_item in set_object.items_missing:

            if missing_item in list_of_new_items:

                move_these_items.append(missing_item)

            else:

                keep_these_in_missing.append(missing_item)

        # Update the set object
        set_object.items_missing = keep_these_in_missing
        set_object.items_matching.extend(move_these_items)
        set_object.calculate_percent_match()

    return all_potential_sets


##############################################################################
############################# More testing ###################################
##############################################################################

"""
THIS TEST WORKS
Testing the return_updated_sets function when we directly pass in a small set of values to it


a = Set("62448472")
a.items_missing = ['49816691','64319388','67802164']
a.items_matching = ['29524227', '65342355']
a.calculate_total_items()
a.calculate_percent_match()

print "**********************"
print a
print "original items matching"
print a.items_matching
print "original items missing"
print a.items_missing
print "percent match"
print a.percent_match
print "**********************"

before = {"62448472": a}

print "**********************"
print "BEFORE"

for key, set_object in before.iteritems():
    print set_object.items_matching
    print set_object.items_missing
    print set_object.percent_match

print "**********************"

list_of_new_items = ['64319388', '67802164', '49816691']

after = return_updated_sets(before, list_of_new_items)

print "**********************"
print "AFTER"

for key, set_object in after.iteritems():
    print set_object.items_matching
    print set_object.items_missing
    print set_object.percent_match

print "**********************"
"""

##############################################################################
############################# Testing Vars ###################################
##############################################################################

"""
THIS TEST ALSO WORKS
Testing the whole process as it should be passed in from Flask

db = connect_db()

selected_inventory_test = ["68519560", "64888102",
"69029707",
"65176054",
"67009179",
"64181961",
"65342355",
"64108504",
"67244905",
"65232087",
"63396515",
"67365763",
"43907865",
"59764503",
"31438308",
"34129315",
"15067690",
"29524227",
"59704080",
"46179180",
"31432829",
"59174684",
"10485009",
"60055493",
"59282239"]

test_all_potential = all_potential_sets(db, selected_inventory_test)

a_original = test_all_potential['62448472']

print "**********************"
print a_original
print "original items matching"
print a_original.items_matching
print "original items missing"
print a_original.items_missing
print "percent match"
print a_original.percent_match

test_suggested_items = get_suggested_items(test_all_potential)

test_newly_selected_items = ['64319388','49816691', '67802164']

test_all_potential = return_updated_sets(test_all_potential, test_newly_selected_items)

a_updated = test_all_potential['62448472']

print "**********************"
print a_updated
print "updated items matching"
print a_updated.items_matching
print "updated items missing"
print a_updated.items_missing
print "percent match"
print a_updated.percent_match
print "**********************"

"""




















