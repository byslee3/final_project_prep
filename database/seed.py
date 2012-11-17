import model
import polyvore
import time

# This should be read in consecutive order downwards
# Records the steps that we took to seed the database

"""
SEED BATCH
Top 5 sets from Tuesday Nov 6

http://www.polyvore.com/sin_t%C3%ADtulo_892/set?id=62332524
http://www.polyvore.com/popular_trend_plaid_bag/set?id=62652167
http://www.polyvore.com/am_who_because_my_choices/set?id=62652303
http://www.polyvore.com/untitled_237/set?id=62655046
http://www.polyvore.com/untitled_205/set?id=62660147

"""


#############################
# Start with seed batch
# Last pulled Thu Nov 15
#############################

batch_1 = [
("62332524", "sin_t%C3%ADtulo_892"),
("62652167", "popular_trend_plaid_bag"),
("62652303", "am_who_because_my_choices"),
("62655046", "untitled_237"),
("62660147", "untitled_205")
]

def pull_sets(batch):

    counter = 0

    for set_id, seo_title in batch:
        
        polyvore.create_set_file(set_id, seo_title)
        print "file %d created" % counter
        time.sleep(1)
        counter += 1

# pull_sets(batch_1)


#############################
# Pull the pages that store Sets --> Fans
# Last pulled Thu Nov 15
#############################

def pull_set_fan_linkages(batch):

    for set_id, seo_title in batch:

        polyvore.create_set_fan_files(set_id)

        print "file successfully created"

# pull_set_fan_linkages(batch_1)


#############################
# Populate the Sets_Fans table in the database
# Last performed Thu Nov 15
#############################

def populate_sets_fans(batch):
    
    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_sets_fans(db, set_id)

# populate_sets_fans(batch_1)


#############################
# Populate the Sets_Items table in the database
# Last performed Thu Nov 15
#############################

def populate_sets_items(batch):
    
    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_sets_items(db, set_id)

# populate_sets_items(batch_1)


#############################
# Prelim analytics
# See degree of overlap between fans of top 5 sets
#############################

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


#############################
# Pull a list of unique fan_names from the Sets_Fans table
# Pull a list of unique items from the Sets_Items table
# These can be abstracted into one function later on
#############################

def list_of_unique_fans(batch):

    """ Return a list of unique fan names which will be passed to create_file function """

    # Make a tuple of the relevant sets to pass into the query
    relevant_sets = tuple([ b[0] for b in batch ])
    question_marks = ["?"] * len(relevant_sets)
    question_marks_string = ", ".join(question_marks)

    # Format and execute the SQL query
    db = model.connect_db()
    query_template = """SELECT DISTINCT fan_name FROM Sets_Fans WHERE set_id IN (%s)"""
    query = query_template % (question_marks_string)
    result = db.execute(query, relevant_sets)
    
    # Get a list of records and return it
    list_of_fans = [ row[0] for row in result.fetchall() ]
    return list_of_fans


def list_of_unique_items(batch):

    """ Return a list of unique items as (item_id, item_seo_title) which will be passed to create_file function """

    # Make a tuple of the relevant sets to pass into the query
    relevant_sets = tuple([  b[0] for b in batch  ])
    question_marks = ["?"] * len(relevant_sets)
    question_marks_string = ", ".join(question_marks)

    # Format and execute the SQL query
    db = model.connect_db()
    query_template = """SELECT DISTINCT item_id, item_seo_title FROM Sets_Items WHERE set_id IN (%s)""" 
    query = query_template % (question_marks_string)
    result = db.execute(query, relevant_sets)

    # Get a list of records and return it
    list_of_items = [ row for row in result.fetchall() ]
    return list_of_items


#############################
# Pull all the Fans associated with a given set
# Pull all the Items associated with a given set
# Last performed Thu Nov 15
#############################

list_of_fan_names = list_of_unique_fans(batch_1)    # 1171 records
list_of_items = list_of_unique_items(batch_1)       # 32 records


def pull_users(list_of_fan_names):

    counter = 0

    for name in list_of_fan_names:

        polyvore.create_user_file(name)
        print "file %d created" % counter
        time.sleep(1)
        counter += 1


def pull_items(list_of_items):

    counter = 0

    for item_id, item_seo_title in list_of_items:

        polyvore.create_item_file(item_id, item_seo_title)
        print "file %d created" % counter
        time.sleep(.25)
        counter += 1


# pull_users(list_of_fan_names) ---> last run Nov 15
# pull_items(list_of_items) ---> last run Nov 15


#############################
# Enter the Fans into the database
# Assign them as Level 2
# But break it up into Level 2.1, 2.2, 2.3 so you can run them in smaller batches
#############################

# -----> Populated on Nov 15

def whatever():

    db = model.connect_db()

    for i in range(0, 300):
        print list_of_fan_names[i]
        model.enter_new_user(db, list_of_fan_names[i], 2.1)

    for i in range(300, 600):
        print list_of_fan_names[i]
        model.enter_new_user(db, list_of_fan_names[i], 2.2)

    for i in range(600, 900):
        print list_of_fan_names[i]
        model.enter_new_user(db, list_of_fan_names[i], 2.3)

    for i in range(900, len(list_of_fan_names)):
        print list_of_fan_names[i]
        model.enter_new_user(db, list_of_fan_names[i], 2.4)

#############################
# Enter the Items into the database
# Assign them as Level 2
#############################

def populate_items(item_list, level):

    db = model.connect_db()

    for item_id, item_seo_title in item_list:

        print item_id

        model.enter_new_item(db, item_id, level)


# populate_items(list_of_items, 2) --> last run Nov 15


def unique_item_id(batch):

    # SELECT query based on batch = 1
    # Copy the list_of_unique_items function above
    # For now, do the shortcut

    result = [  item[0] for item in list_of_unique_items(batch)  ]
    return result


#############################
# Populate the Items_Sets table in the database
# Tag all these records with level = 2
# Last performed Thu Nov 15
#############################

list_1 = unique_item_id(batch_1)

def populate_items_sets(list_of_ids):

    db = model.connect_db()

    for item_id in list_of_ids:

        model.enter_new_items_sets(db, item_id)

# populate_items_sets(list_1)


#############################
# Get a list of unique sets from Items_Sets
# Last performed Thu Nov 15
#############################

def list_of_unique_sets(level):

    """ Return a list of unique sets as (set_id, set_seo_title) which will be passed to create_file function """

    # Format and execute the SQL query
    db = model.connect_db()
    query = """SELECT DISTINCT set_id, set_seo_title FROM Items_Sets WHERE level = ?"""
    result = db.execute(query, (level,))

    # Get a list of records and return it
    list_of_sets = [ row for row in result.fetchall() ]
    return list_of_sets


#############################
# Pull all the sets
# Assign them to Level 3
# Last performed Thu Nov 15
#############################

level_3 = list_of_unique_sets(2)

# pull_sets(level_3) ---> last run Nov 15


#############################
# Enter the seed sets and the Level 3 sets into the database
#############################

# -----> Populated Nov 15

def whatever2():

    db = model.connect_db()

    for set_id, set_seo_title in batch_1:
        try:
            model.enter_new_set(db, set_id, 1)
        except IOError:
            print "No file exists (likely Unicode Error)"

    for set_id, set_seo_title in level_3:
        try:
            model.enter_new_set(db, set_id, 3)
        except IOError:
            print "No file exists (likely Unicode Error)"


#############################
# Grab all the Fan --> Item relationships from Level 2
#############################


db = model.connect_db()

query1 = """SELECT DISTINCT user_id FROM Users WHERE level = 2.1"""
query2 = """SELECT DISTINCT user_id FROM Users WHERE level = 2.2"""
query3 = """SELECT DISTINCT user_id FROM Users WHERE level = 2.3"""
query4 = """SELECT DISTINCT user_id FROM Users WHERE level = 2.4"""

result1 = db.execute(query1)
result2 = db.execute(query2)
result3 = db.execute(query3)
result4 = db.execute(query4)

list_fans_1 = [  row[0] for row in result1.fetchall()  ]
list_fans_2 = [  row[0] for row in result2.fetchall()  ]
list_fans_3 = [  row[0] for row in result3.fetchall()  ]
list_fans_4 = [  row[0] for row in result4.fetchall()  ]

# print list_fans_1
# print list_fans_2
# print list_fans_3
# print list_fans_4
# print len(list_fans_1)
# print len(list_fans_2)
# print len(list_fans_3)
# print len(list_fans_4)

# for i, user_id in enumerate(list_fans_4):

#     polyvore.create_user_items_files(user_id)
#     print "file %d created" % i
#     time.sleep(.5)

# -----> Ran all of this on Nov 15


#############################
# Take all the Fan-Item relationships and put them into the database at Level 2
#############################

# for fan_id in list_fans_4:
#     model.enter_new_users_items(db, fan_id, 2)

# -----> Populated the database on Nov 16


#############################
# Get the list of unique items
#############################

table = "Users_Items"
col = "item_id"
col1 = "item_id"
col2 = "item_seo_title"
level = 2


def unique_records_onecol(table, col, level):

    # Format and execute the SQL query
    db = model.connect_db()
    query_template = """SELECT DISTINCT (%s) FROM (%s) WHERE level = (%d)""" 
    query = query_template % (col, table, level)
    result = db.execute(query)

    # Get a list of records and return it
    list_of_items = [ row[0] for row in result.fetchall() ]
    return list_of_items


def unique_records_twocol(table, col1, col2, level):

    # Format and execute the SQL query
    db = model.connect_db()
    query_template = """SELECT DISTINCT (%s), (%s) FROM (%s) WHERE level = (%d)""" 
    query = query_template % (col1, col2, table, level)
    result = db.execute(query)

    # Get a list of records and return it
    list_of_items = [ row for row in result.fetchall() ]
    return list_of_items



#############################
# Pull down the item files in batches
#############################

# 43045 unique records
list_to_pull = unique_records_twocol("Users_Items", "item_id", "item_seo_title", 2)

# split the list to pull into batches of approx 5K

l0 = []
l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []
l7 = []
l8 = []
l9 = []

temp_dict = {'0': l0, '1': l1, '2':l2, '3': l3, '4': l4, '5':l5, '6': l6, '7':l7, '8':l8, '9':l9}

for tup in list_to_pull:

    lastnum = tup[0][-1]

    target_list = temp_dict[lastnum]

    target_list.append(tup)


#### Run each list through this once
#### Last run on Nov 16

# pull_items(l0) --> already ran l0

# still need to run l1 through l9 which will take approx 3 hours


#############################
# Enter the items into the database with Level 3
#############################

# Run this for l0 through l9
# populate_items(l0, 3) --> last run Nov 15








