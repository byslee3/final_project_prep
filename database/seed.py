import model
import polyvore

# This should be read in consecutive order downwards
# Records the steps that we took to seed the database


#####
# Started with first batch of top 5 sets
# From Tuesday Nov 6

batch_1 = [

(62332524, "sin_t%C3%ADtulo_892"),
(62652167, "popular_trend_plaid_bag"),
(62652303, "am_who_because_my_choices"),
(62655046, "untitled_237"),
(62660147, "untitled_205")

]


#####
# Pull this batch from Polyvore
# Last run on Friday Nov 9
# RUN THIS AS LITTLE AS POSSIBLE

def pull(batch):

    for set_id, seo_title in batch:
        
        polyvore.create_set_file(set_id, seo_title)

# pull(batch_1)


#####
# Populate the Sets table for this batch

def populate_sets(batch):

    db = model.connect_db()

    for set_id, seo_title in batch:

        model.enter_new_set(db, set_id)

# populate_sets(batch_1)


#####
# Checking that we're able to get the fan URLs

print polyvore.get_set_fans_url(62332524)
print polyvore.get_set_fans_url(62332524)








