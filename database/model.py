import sqlite3
import polyvore


COLUMNS_SET = [
"set_id",
"seo_title",
"title",
"anchor",
"set_type",
"creator_id",
"creator_name",
"created_on",
"imgurl",
"score",
"pageviews",
"num_fans",
"num_items_all",
"num_items_valid"
]

COLUMNS_SETS_FANS = [
"set_id",
"fan_id",
"fan_name"
]


def connect_db():
    return sqlite3.connect("polyvore.db")


def enter_new_set(db, set_id):

    # Get all the set attributes in dictionary form from the JSON file
    d = polyvore.get_set_attributes(set_id)

    # Pull out all the values and create a tuple that can be passed to SQL query
    values_to_add = []
    global COLUMNS_SET

    for column in COLUMNS_SET:

        value = d[column]
        values_to_add.append(value)

    values_to_add = tuple(values_to_add)

    # Use SQL query to add these attributes as a new record in the database
    c = db.cursor()
    query = """INSERT INTO Sets VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    c.execute(query, values_to_add)
    db.commit()


def enter_new_sets_fans(db, set_id):

    ## Update the Sets_Fans table
    ## For a given set_id, enter all of the fan_ids and fan_names that are associated with it
    ## The Sets_Fans table maps a many-to-many relationship between each set and users that Fanned the set

    # For this set_id: Get a list of tuples, storing all the associated fan_ids and fan_names
    values_to_add = polyvore.get_set_fans(set_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Sets_Fans VALUES(NULL, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (set_id, v[0], v[1]))

    db.commit()


def enter_new_sets_items(db, set_id):

    ## Update the Sets_Items table
    ## For a given set_id, enter all of the item_ids that are associated with it
    ## The Sets_Items table maps a many-to-many relationship between each set and items that are in the set

    # For this set_id: Get a list of tuples, storing all the associated fan_ids and fan_names
    values_to_add = polyvore.get_set_items(set_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Sets_Items VALUES(NULL, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (set_id, v[0], v[1]))

    db.commit()



























