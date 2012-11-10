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





























