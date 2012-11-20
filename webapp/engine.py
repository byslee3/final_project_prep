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


def get_starting_items():

    # In the future: Will return list of 100 items to be displayed
    # As starting point for user's inventory

    # RETURN DUMMY DATA FOR NOW
    test = ["11111", "22222", "33333", "44444", "55555", "66666", "77777"]
    return test


def return_matching_sets(selected_inventory):

    # Takes a list of items that the user has selected as being in the inventory
    # Goes through all the sets in the database and finds the matching ones

    # -----> To make it run quickly for now, only go through first 5,000 sets

    # -----> This is going to need to call a bunch of sub-functions (see diagram in notebook)
    # -----> Rank the sets by % match, or have a cutoff (put this in sub-function)

    # RETURN DUMMY DATA FOR NOW
    # Ultimately return a list of set objects that contains lots of different data that I need
    # (so that we don't have to call this function over and over)
    result = ["setA_obj", "setB_obj", "setC_obj", "setD_obj", "setE_obj"]
    return result


def return_updated_sets(existing_sets, new_item):

    # Take the existing list of set objects
    # Take the new item and move it from the attribute:missing item >>> to the attribute:matching items
    # Recalculate the matching percentages

    # RETURN DUMMY DATA FOR NOW
    result = ["setA_obj", "setB_obj", "setC_obj", "setD_obj", "setE_obj"]
    return result














