import sqlite3
import polyvore


# Variables for testing

SET1 = "62332524"
SET2 = "62652167"
SET3 = "62652303"
SET4 = "62655046"
SET5 = "62660147"

FAN1 = "3339312"
FAN2 = "3159094"
FAN3 = "1231532"

ITEM1 = "17109441"

# Column field headings
# Need this for pulling stuff out of the dictionary

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
]   # Also have "level" variable at the end but it is passed in separately

COLUMNS_ITEM = [
"item_id",
"seo_title",
"title",
"anchor",
"age",
"imgurl",
"save_count",
"category_id",
"brand_id",
"brand_name",
"usd_price",
"retailer"
]   # Also have "level" variable at the end but it is passed in separately

COLUMNS_USER = [
"user_id",
"user_name",
"country",
"createdon_ts"
]   # Also have "level" variable at the end but it is passed in separately



def connect_db():
    return sqlite3.connect("polyvore.db")


def enter_new_set(db, set_id, level):

    # Get all the set attributes in dictionary form from the JSON file
    d = polyvore.get_set_attributes(set_id)

    # Pull out all the values and create a tuple that can be passed to SQL query
    values_to_add = []
    global COLUMNS_SET

    for column in COLUMNS_SET:
        value = d[column]
        values_to_add.append(value)

    values_to_add.append(level)   # Marker that we use for determining which batch it was pulled in
    values_to_add = tuple(values_to_add)

    # Use SQL query to add these attributes as a new record in the database
    c = db.cursor()
    query = """INSERT INTO Sets VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    c.execute(query, values_to_add)
    db.commit()


def enter_new_item(db, item_id, level):

    # Get all the item attributes in dictionary form from the JSON file
    d = polyvore.get_item_attributes(item_id)

    # Pull out all the values and create a tuple that can be passed to SQL query
    values_to_add = []
    global COLUMNS_ITEM

    for column in COLUMNS_ITEM:
        value = d.get(column, None)
        values_to_add.append(value)

    values_to_add.append(level)   # Marker that we use for determining which batch it was pulled in
    values_to_add = tuple(values_to_add)

    # Use SQL query to add these attributes as a new record in the database
    c = db.cursor()
    query = """INSERT INTO Items VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    c.execute(query, values_to_add)
    db.commit()


def enter_new_user(db, user_name, level):

    # Get all the user attributes in dictionary form from the JSON file
    d = polyvore.get_user_attributes(user_name)

    # Pull out all the values and create a tuple that can be passed to SQL query
    values_to_add = []
    global COLUMNS_USER

    for column in COLUMNS_USER:
        value = d.get(column, None)
        values_to_add.append(value)

    values_to_add.append(level)   # Marker that we can use for determining which batch it was pulled in
    values_to_add = tuple(values_to_add)

    # Use SQL query to add these attributes as a new record in the database
    c = db.cursor()
    query = """INSERT INTO Users VALUES(NULL, ?, ?, ?, ?, ?)"""
    c.execute(query, values_to_add)
    db.commit()


def enter_new_sets_fans(db, set_id, level):

    ## Update the Sets_Fans table
    ## For a given set_id, enter all of the fan_ids and fan_names that are associated with it
    ## The Sets_Fans table maps a many-to-many relationship between each set and users that Fanned the set

    # For this set_id: Get a list of tuples, storing all the associated fan_ids and fan_names
    values_to_add = polyvore.get_set_fans(set_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Sets_Fans VALUES(NULL, ?, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (set_id, v[0], v[1], level))

    db.commit()


def enter_new_sets_items(db, set_id, level):

    ## Update the Sets_Items table
    ## For a given set_id, enter all of the item_ids that are associated with it
    ## The Sets_Items table maps a many-to-many relationship between each set and items that are in the set

    # For this set_id: Get a list of tuples, storing all the associated fan_ids and fan_names
    values_to_add = polyvore.get_set_items(set_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Sets_Items VALUES(NULL, ?, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (set_id, v[0], v[1], level))

    db.commit()


def enter_new_fans_sets(db, fan_id, level):

    ## Update the Fans_Sets table
    ## For a given user_id, enter all of the set_ids and set_seo_titles that are associated with it
    ## =====> Can be merged with Sets_Fans later but keep it separate for now

    # For this fan_id: Get a list of tuples with (a) set_id (b) set_seo_title
    values_to_add = polyvore.get_user_sets(fan_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Fans_Sets VALUES(NULL, ?, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (fan_id, v[0], v[1], level))

    db.commit()


def enter_new_users_items(db, user_id, level):

    ## Update the Users_Items table
    ## For a given user_id, enter all of the item_ids and item_seo_titles that are associated with it

    # For this user_id: Get a list of tuples with (a) item_id (b) item_seo_title
    values_to_add = polyvore.get_user_items(user_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Users_Items VALUES(NULL, ?, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (user_id, v[0], v[1], level))

    db.commit()


def enter_new_items_sets(db, item_id, level):

    ## Update the Items_Sets table
    ## For a given item_id, enter all of the set_ids and set_seo_titles that are associated with it
    ## =====> Can be merged with Sets_Items later but keep it separate for now

    # For this specific item_id: Get a list of tuples with (a) set_id (b) set_seo_title
    values_to_add = polyvore.get_item_sets(item_id)

    # Loop through all the values_to_add and insert them into database
    c = db.cursor()
    query = """INSERT INTO Items_Sets VALUES(NULL, ?, ?, ?, ?)"""

    for v in values_to_add:
        c.execute(query, (item_id, v[0], v[1], level))

    db.commit()



























