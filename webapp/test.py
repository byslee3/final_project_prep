import sqlite3
import random


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











