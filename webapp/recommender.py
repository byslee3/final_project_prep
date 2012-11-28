from flask import Flask, render_template, redirect, request, session, flash, g
import engine
import sqlite3
import test
import engine2


#############################
###### Setup / Generic ######
#############################

DATABASE = "polyvore.db"

# Initialize app
app = Flask(__name__)
app.config.from_object(__name__)

# Database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


#############################
##### Global Variables ######
#############################

""" Is there a way to get data from webpage without using these? """

selected_inventory = []




#############################
######## Functions ##########
#############################


@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/clear_inventory")
def clear_inventory():
    global selected_inventory
    selected_inventory = []
    return redirect("/start")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():

    starting_inventory = engine2.get_starting_items(g.db)
    name = request.form['user_name']
    initial_round = True

    return render_template("inventory.html", 
        potential_inventory = starting_inventory, 
        name = name, 
        initial_round=True)


@app.route("/next_inventory", methods=["GET", "POST"])
def next_inventory():

    global selected_inventory

    if len(selected_inventory) < 19:

        # Enter this round's selection into the selected_inventory
        this_round_selection = request.form.keys()
        selected_inventory.extend(this_round_selection)

        # Get the next round of potential inventory and render template
        next_inventory = engine2.get_next_items(g.db, this_round_selection, selected_inventory)

        return render_template("inventory.html",
            potential_inventory = next_inventory,
            initial_round = False,
            this_round_selection = this_round_selection,
            total_inventory = selected_inventory)

    else:

        # Go to the part where they return the sets
        return redirect("/before_combinations")


@app.route("/before_combinations", methods=["GET"])
def before_combinations():

    global selected_inventory

    return render_template("before_combinations.html", 
        selected_inventory = selected_inventory)


@app.route("/combinations", methods=["GET", "POST"])
def combinations():

    global selected_inventory

    # Get a list of set objects that match
    result_dictionary = engine2.return_matching_sets(g.db, selected_inventory)

    result_test = []
    for key, set_obj in result_dictionary.iteritems():
        result_test.append(set_obj)


    # Pull out the set URLs from the set objects (need to implement)
    existing_sets = []

    for key, set_obj in result_dictionary.iteritems():
        set_id = set_obj.set_id   # In the future, pull the set URL instead
        existing_sets.append(set_id)

    # Pull out the suggested items from the set objects (need to implement)
    suggested_items = ["d", "e", "f"]  # This will be an attribute in the future

    return render_template("combinations.html",
        selected_inventory = selected_inventory,
        existing_sets = existing_sets,
        suggested_items = suggested_items,
        result_test = result_test)  # Pass the entire result dictionary in for testing purposes


@app.route("/update_combinations", methods=["GET", "POST"])
def update_combinations():

    """ ?????????????? """
    """ Need to figure out this part """
    """ ?????????????? """
    existing_sets = "x"  # -----> How to grab this from inventory.html?
    new_item = "x"  # -----> How to grab this from inventory.html?

    updated_result = engine.return_updated_sets(existing_sets, new_item)

    """ Should be able to pull these out from the updated_result list"""
    selected_inventory = ["temp1", "temp2", "temp3", "temp4", "temp5"]
    suggested_items = ["itemA", "itemB", "itemC"]

    return render_template(
        "combinations.html", 
        selected_inventory=selected_inventory, 
        existing_sets=existing_sets, 
        suggested_items=suggested_items)














# App starts running here
if __name__ == "__main__":
    app.run(debug = True)







