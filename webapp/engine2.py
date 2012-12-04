import sqlite3
import random
from operator import itemgetter


##############################################################################
########################### Class Definition #################################
##############################################################################

class Set(object):

    def __init__(self, set_id, imgurl=None):
        self.set_id = set_id
        self.imgurl = imgurl
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

    def __init__(self, item_id, imgurl=None):
        self.item_id = item_id
        self.imgurl = imgurl

    def get_imgurl(self, db):
        cur = db.cursor()
        query = """SELECT imgurl FROM Items WHERE item_id = ?"""
        query_result = cur.execute(query, (self.item_id,))
        self.imgurl = cur.fetchone()[0]


# If needs to be called from recommender.py --> Figure out later where to put this
def create_entire_item(item_id, db):

    new_item_object = Item(item_id)
    new_item_object.get_imgurl(db)
    return new_item_object

# Testing if the get_imgurl function works
def test6():

    db = connect_db()

    new_item = Item("60387619")

    new_item.get_imgurl(db)

    print new_item.item_id
    print new_item.imgurl



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
        item.get_imgurl(db)   # Runtime: queries the database. Only < 4 items right now.
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

    """
    FIX THIS LATER
    For now -- cap the num of items returned at 40, otherwise the runtime is too long G;LKAJERLAKEJRLKEJ
    """
    if num_groups > 10:
        num_groups = 10

    """
    Take out everything between this and the last block comment
    """

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
    # In the future, I should query from Items directly so that I don't have to join tables, it will be faster
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
        item.get_imgurl(db)   # Runtime: queries the database. Only 8 items for now.
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
                item_object.get_imgurl(db)  # ---> FIX THIS --> Runtime: queries the database. Could be 100+ items. It's slowing down the webapp.
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
        set_imgurl = record[5]

        # If the set has not been recorded yet, create a new set object and store in dictionary
        if d.get(set_id) == None:

            d[set_id] = Set(set_id, set_imgurl)

            # Determine whether the item is a matching or missing item, and update the Set object accordingly
            if item_id in selected_inventory:
                d[set_id].items_matching.append(item_id)
            else:
                d[set_id].items_missing.append(item_id)

        else:
            # Determine whether the item is a matching or missing item, and update the Set object accordingly
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

    cutoff_percent = 50.0

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

def is_set_movable(set_object, cutoff):

    """
    Return -1 if set is already over the cutoff
    Return 0 if moving one item will not bump the set over
    Return 1 if moving one item WILL bump the set over
    """

    if set_object.percent_match >= cutoff:
        return -1

    else:

        hypothetical_items_matching = len(set_object.items_matching) + 1.0
        hypothetical_percent_match = round(hypothetical_items_matching / set_object.total_items * 100, 1)

        if hypothetical_percent_match >= cutoff:
            return 1

        else:
            return 0


# Testing the is_set_movable function -- it works!
def test4():

    test_cutoff = 75.0

    a = Set("already matched")
    a.items_matching = [1, 2, 3]
    a.items_missing = [4]
    a.calculate_total_items()
    a.calculate_percent_match()

    b = Set("movable")
    b.items_matching = [1]
    b.items_missing = [2, 3]
    b.calculate_total_items()
    b.calculate_percent_match()

    c = Set("not movable")
    c.items_matching = [1]
    c.items_missing = [2, 3, 4, 5]
    c.calculate_total_items()
    c.calculate_percent_match()

    d = Set("movable 2")
    d.items_matching = [1]
    d.items_missing = [2, 3, 4]
    d.calculate_total_items()
    d.calculate_percent_match()

    print is_set_movable(a, test_cutoff)
    print is_set_movable(b, test_cutoff)
    print is_set_movable(c, test_cutoff)
    print is_set_movable(d, test_cutoff)


def create_item_table(all_potential_sets, cutoff):

    """
    Pass in all_potential_sets: dictionary where each entry is {set_id: set_object}
    Pass in cutoff: float denoting the cutoff percentage for a set to match
    Returns a list of tuples, where each entry is (col1, col2, col3) etc as following the below
    """
    # Create the item table with the following columns in each row:
    # Records will only be created for MISSING items
    #   Column0 = item_id
    #   Column1 = the set that it belongs to
    #   Column2 = current percent match of the set
    #   Column3 = difference between the percent match and the cutoff
    #   Column4 = would moving one item bump the set over the cutoff?
    #   Column5 to 8 = leave in now for debugging
    # Some of these columns we may not have to use, but just create them now just in case

    item_table = []

    for key, set_object in all_potential_sets.iteritems():

        set_id_test = set_object.set_id   # This is really only needed for testing, makes no difference to the end answer
        set_percent_match = set_object.percent_match
        set_difference = cutoff - set_percent_match
        set_movable = is_set_movable(set_object, cutoff)

        for item_id in set_object.items_missing:

            table_row = tuple([item_id, set_id_test, set_percent_match, set_difference, set_movable, "matching", len(set_object.items_matching), "missing", len(set_object.items_missing)])
            item_table.append(table_row)

    return item_table


# Testing the create_item_table function -- it works!
def test5():

    db = connect_db()
    selected_inventory_test = ["60387619", "67807105", "31221171", "49922912",
    "49881679", "37322442", "65354882", "577750497", "48899525", "55486970",
    "34514286", "53078281", "56072045", "51474209", "31237490", "27930863",
    "66546372", "61086925", "61190827", "20772992", "63797724", "17719636",
    "56200379", "66804821"]
    all_potential_sets_test = all_potential_sets(db, selected_inventory_test)

    test_answer = create_item_table(all_potential_sets_test, 75.0)

    for row in test_answer:
        print row

    print "length of table is %d items" % len(test_answer)


def get_suggested_items(all_potential_sets, cutoff, db):

    """
    Takes in the following arguments:
        Pass in a dictionary of {set_id: set_object}
        Pass in cutoff as a float, where 75.0% cutoff is passed in as 75.0
        Pass in items_already_selected, which is a list of item ids ["34234", "34559", "342098"]
    Pick the top 16 suggested items
    Return a list of item Objects, grouped into fours: [[obj1, obj2, obj3, obj4], [obj5, obj6, obj7, obj8]]
    ---> CONTINUE TO REFINE THIS FUNCTION LATER. THIS CAN USE A LOT OF REFINEMENT.
            ---> Weight an item more heavily if it helps bump 2+ sets over the cutoff
            ---> This could go on infinitely? Would have to update the hypothetical inventory and pull new matching sets each time
            ---> Runtime implications
    """

    """
    Step 1: Get the item table
    Step 2: Select only those items belonging to sets that are movable
    Step 3: Rank order all the records by proximity to cutoff
    Step 4: Select the top 16, accounting for dups
    Step 5: Format list and return
    """

    ### Step 1: Get the item table
    item_table = create_item_table(all_potential_sets, cutoff)

    ### Step 2: Select only those items belonging to sets that are movable
    item_table_movable = []

    for row in item_table:
        if row[4] == 1:
            item_table_movable.append(row)

    ### Step 3: Rank order all the records by proximity to cutoff
    item_table_sort1 = sorted(item_table_movable, key=itemgetter(3))

    """ Here is where we could refine: Sort them on something else, since the top ~20 records are indistinguishable right now """

    ### Step 4: Select the top 8, accounting for dups

    """ Another place to refine. Should choose items from different sets."""
    """Because if you choose all 3 items from the closest matched set, it will still only bump one set over the cutoff."""

    result = []
    result_keys_only = []
    index = 0

    while index < len(item_table_sort1):  # Sometimes item_table_sort1 is very short and there aren't even 8 suggested items

        if len(result) == 8:  # Max 8 spaces
            break

        else:
            item_id = item_table_sort1[index][0]

            if not item_id in result_keys_only:
                suggested_item = Item(item_id)
                suggested_item.get_imgurl(db)  # Runtime: this queries the database. Only 8 times for now.
                result.append(suggested_item)
                result_keys_only.append(item_id)

            index += 1

    # ----> Need to get some extra items if item_table_sort1 is not long enough
    if len(result) < 8:
        num_to_get = 8 - len(result)
        additional_items = get_random_items(db, num_to_get)  # Returns a list of item objects
        result.extend(additional_items)

    # Step 5: Format list and return. Make sure you always pass it a list of 4*n entries!
    formatted_result = format_list(None, result)   # Pass it dummy variable for db since we don't need it, Python won't check type

    return formatted_result


# Testing for the get_suggested_items function -- works in Python!
def test3():

    db = connect_db()
    selected_inventory_test = ["60387619", "67807105", "31221171", "49922912",
    "49881679", "37322442", "65354882", "577750497", "48899525", "55486970",
    "34514286", "53078281", "56072045", "51474209", "31237490", "27930863",
    "66546372", "61086925", "61190827", "20772992", "63797724", "17719636",
    "56200379", "66804821"]
    all_potential_sets_test = all_potential_sets(db, selected_inventory_test)
    matching_sets = return_matching_sets(db, all_potential_sets_test)

    suggested_items = get_suggested_items(all_potential_sets_test, 75.0, db)

    print suggested_items


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
"641087504",
"67244905",
"65232087",
"63396515",
"67365763",
"43907865",
"597647503",
"31438308",
"34129315",
"175067690",
"29524227",
"59704080",
"46179180",
"31432829",
"59174684",
"104875009",
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




















