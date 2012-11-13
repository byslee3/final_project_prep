import model
import polyvore

# This should be read in consecutive order downwards
# Records the steps that we took to seed the database

"""
http://www.polyvore.com/sin_t%C3%ADtulo_892/set?id=62332524
http://www.polyvore.com/popular_trend_plaid_bag/set?id=62652167
http://www.polyvore.com/am_who_because_my_choices/set?id=62652303
http://www.polyvore.com/untitled_237/set?id=62655046
http://www.polyvore.com/untitled_205/set?id=62660147

"""

#####
# Started with first batch of top 5 sets
# From Tuesday Nov 6

batch_1 = [

("62332524", "sin_t%C3%ADtulo_892"),
("62652167", "popular_trend_plaid_bag"),
("62652303", "am_who_because_my_choices"),
("62655046", "untitled_237"),
("62660147", "untitled_205")

]


#####
# Pull this batch from Polyvore
# Last run on Friday Nov 9
# RUN THIS AS LITTLE AS POSSIBLE

def pull_sets(batch):

    for set_id, seo_title in batch:
        
        polyvore.create_set_file(set_id, seo_title)

# pull_sets(batch_1)


#####
# Populate the Sets table for this batch

def populate_sets(batch):

    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_set(db, set_id)

# populate_sets(batch_1)


#####
# Pull the set_fans pages from Polyvore
# Last run on Monday Nov 12
# RUN THIS AS LITTLE AS POSSIBLE

def pull_set_fans(batch):

    for set_id, seo_title in batch:

        polyvore.create_set_fan_files(set_id)

        print "file successfully created"

# pull_set_fans(batch_1)


#####
# Populate the Sets_Fans table for batch 1

def populate_sets_fans(batch):
    
    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_sets_fans(db, set_id)

# populate_sets_fans(batch_1)


#####
# Preliminary analytics

def print_overlap():

    db = model.connect_db()

    # Creates a table with 2 columns -- (a) fan_name (b) num out of 5 sets in batch_1 that they fanned
    cursor = db.execute("SELECT fan_name, COUNT(fan_name) FROM Sets_Fans GROUP BY fan_name")

    # Doing the rest in Python instead of SQL for now --> need to look up how to query the result of a query
    total_fans = 0.0
    sets_rated_by_each_fan = ["Not Applicable", 0.0, 0.0, 0.0, 0.0, 0.0]

    for row in cursor.fetchall():

        number_rated = row[1]
        sets_rated_by_each_fan[number_rated] += 1

        total_fans += 1

    # Transform frequency counts into percentages

    print "LEVEL OF OVERLAP"
    print "Out of " + str(int(total_fans)) + " total fans who rated 5 'Popular' sets"
    print "--------------------------------------------------"

    for x in range(1,6):
        percentage = int(round(sets_rated_by_each_fan[x]/total_fans*100))
        print str(int(sets_rated_by_each_fan[x])) + " out of " + str(int(total_fans)) + " -- (" + str(percentage) + "%) -- rated " + str(x) + " out of 5 sets"

# print_overlap()


#####
# Populate the Sets_Items table for batch 1

def populate_sets_items(batch):
    
    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_sets_items(db, set_id)

# populate_sets_items(batch_1)


#####
# Get all of the unique fan names from the Sets_Fans table
# Then pull the actual JSON files for each user and save to text file

""" Delete this function at a later date, use SELECT DISTINCT instead """

def list_of_unique_fans(batch):

    # Make a tuple of the relevant sets to pass into the query
    relevant_sets = tuple([ b[0] for b in batch ])
    question_marks = ["?"] * len(relevant_sets)
    question_marks_string = ", ".join(question_marks)

    # Connecting to database
    db = model.connect_db()

    # Format and execute the SQL query
    query_template = """SELECT * FROM Sets_Fans WHERE set_id IN (%s)"""
    query = query_template % (question_marks_string)
    result = db.execute(query, relevant_sets)
    
    # Get a list of records, where each item is a fan name
    list_of_fans = []

    for row in result.fetchall():

        if not row[3] in list_of_fans:   # Check for duplicates

            if not row[2] == "0":          # If fan_id is 0, means they don't have an actual account

                list_of_fans.append(row[3])

    return list_of_fans


def pull_users(batch):

    list_to_pull = list_of_unique_fans(batch)

    for l in list_to_pull:
        polyvore.create_user_file(l)
        print "file created"

# pull_users(batch_1)
# RUN THIS TOMORROW ALL AT ONCE


#####
# Get all of the unique items from the Sets_Items table
# Then pull the actual JSON files for each user and save to text file
# Decided to re-write this function instead of using code abstraction for this one, need to return list of tuples instead of just one record
# AAAARGH!!! Just remembered the SELECT DISTINCT function..... D:LKFJ*&#$*&^@#%)

""" Delete this function at a later date, use SELECT DISTINCT instead """

def list_of_unique_items(batch):

    # Make a tuple of the relevant sets to pass into the query
    relevant_sets = tuple([ b[0] for b in batch ])
    question_marks = ["?"] * len(relevant_sets)
    question_marks_string = ", ".join(question_marks)

    # Connecting to database
    db = model.connect_db()

    # Format and execute the SQL query
    query_template = """SELECT * FROM Sets_Items WHERE set_id IN (%s)"""
    query = query_template % (question_marks_string)
    result = db.execute(query, relevant_sets)
    
    # Get a list of records, where each item is a fan name
    list_of_item_ids = []
    list_of_item_seo_titles = []

    for row in result.fetchall():

        if not row[2] in list_of_item_ids:  # Check for duplicates
                                            # We need to delay zipping until the end b/c of this.

            list_of_item_ids.append(row[2])
            list_of_item_seo_titles.append(row[3])

    list_of_items = zip(list_of_item_ids, list_of_item_seo_titles)

    return list_of_items


def pull_items(batch):

    list_to_pull = list_of_unique_items(batch)

    for l in list_to_pull:
        polyvore.create_item_file(l)
        print "file created"

# pull_items(batch_1)
# RUN THIS TOMORROW ALL AT ONCE






