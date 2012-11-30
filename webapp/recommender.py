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
""" Or, to have these global variables, but associated with a specific session """

SELECTED_INVENTORY = []
MATCHING_SETS = {}
INITIAL_COMBOS = True
HYPOTHETICAL_MATCHING_SETS = {}
ALL_POTENTIAL_SETS = {}




#############################
######## Functions ##########
#############################


@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/clear_inventory")
def clear_inventory():

    global SELECTED_INVENTORY
    global MATCHING_SETS
    global INITIAL_COMBOS
    global HYPOTHETICAL_MATCHING_SETS
    global ALL_POTENTIAL_SETS

    SELECTED_INVENTORY = []
    MATCHING_SETS = {}
    INITIAL_COMBOS = True
    HYPOTHETICAL_MATCHING_SETS = {}
    ALL_POTENTIAL_SETS = {}

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

    global SELECTED_INVENTORY

    if len(SELECTED_INVENTORY) < 19:

        # Enter this round's selection into the SELECTED_INVENTORY
        this_round_selection = request.form.keys()
        SELECTED_INVENTORY.extend(this_round_selection)

        # Get the next round of potential inventory and render template
        next_inventory = engine2.get_next_items(g.db, this_round_selection, SELECTED_INVENTORY)

        return render_template("inventory.html",
            potential_inventory = next_inventory,
            initial_round = False,
            this_round_selection = this_round_selection,
            total_inventory = SELECTED_INVENTORY)

    else:

        # Go to the part where they return the sets
        return redirect("/before_combinations")


@app.route("/before_combinations", methods=["GET"])
def before_combinations():

    global SELECTED_INVENTORY

    return render_template("before_combinations.html", 
        selected_inventory = SELECTED_INVENTORY)


@app.route("/combinations", methods=["GET", "POST"])
def combinations():

    global INITIAL_COMBOS

    # If it's the first time we are returning matching sets
    if INITIAL_COMBOS:

        global SELECTED_INVENTORY
        global MATCHING_SETS
        global HYPOTHETICAL_MATCHING_SETS
        global ALL_POTENTIAL_SETS

        INITIAL_COMBOS = False

        # Get the matching sets
        # Get a list of potential items
        # Pass them to the render template

        ALL_POTENTIAL_SETS = engine2.all_potential_sets(g.db, SELECTED_INVENTORY)

        MATCHING_SETS = engine2.return_matching_sets(g.db, ALL_POTENTIAL_SETS)

        potential_items = engine2.get_suggested_items(ALL_POTENTIAL_SETS)

        matching_sets_list = []
        for key, set_obj in MATCHING_SETS.iteritems():
            matching_sets_list.append(set_obj)

        print "*****************************"
        print "*****************************"
        print "*****************************"
        print "all_potential_sets"
        print len(ALL_POTENTIAL_SETS)
        for key, value in ALL_POTENTIAL_SETS.iteritems():
            print value
        print "*****************************"
        print "MATCHING_SETS"
        print len(MATCHING_SETS)
        for key, value in MATCHING_SETS.iteritems():
            print value
        print "*****************************"
        print len(potential_items)
        print "potential_items"
        for row in potential_items:
            print row
        print "*****************************"
        print "matching_sets_list"
        print len(matching_sets_list)
        for row in matching_sets_list:
            print row
        print "*****************************"
        print "*****************************"
        print "*****************************"

        return render_template("combinations.html",
            selected_inventory = SELECTED_INVENTORY,
            existing_sets = matching_sets_list,
            suggested_items = potential_items,
            all_potential_sets = ALL_POTENTIAL_SETS,
            which_run = "if statement")


    # Else, we are updating sets
    elif not INITIAL_COMBOS:

        # Get the newly selected items
        # Update the existing sets
        # Check again to see which ones match
        # Get another list of potential items
        # Pass them to the render template
        # ---> Could expand this in the future to call on the database and continue expanding

        newly_selected_items = request.form.keys()
        print "newly selected items"
        print newly_selected_items

        ALL_POTENTIAL_SETS = engine2.return_updated_sets(ALL_POTENTIAL_SETS, newly_selected_items)

        HYPOTHETICAL_MATCHING_SETS = engine2.return_sets_above_cutoff(ALL_POTENTIAL_SETS, 50)

        potential_items = engine2.get_suggested_items(ALL_POTENTIAL_SETS)

        matching_sets_list = []
        for key, set_obj in HYPOTHETICAL_MATCHING_SETS.iteritems():
            matching_sets_list.append(set_obj)

        print "*****************************"
        print "*****************************"
        print "*****************************"
        print "all_potential_sets"
        print len(ALL_POTENTIAL_SETS)
        for key, value in ALL_POTENTIAL_SETS.iteritems():
            print value
        print "*****************************"
        print "HYPOTHETICAL_MATCHING_SETS"
        print len(HYPOTHETICAL_MATCHING_SETS)
        for key, value in HYPOTHETICAL_MATCHING_SETS.iteritems():
            print value
        print "*****************************"
        print len(potential_items)
        print "potential_items"
        for row in potential_items:
            print row
        print "*****************************"
        print "matching_sets_list"
        print len(matching_sets_list)
        for row in matching_sets_list:
            print row
        print "*****************************"
        print "*****************************"
        print "*****************************"

        return render_template("combinations.html",
            selected_inventory = SELECTED_INVENTORY,
            existing_sets = matching_sets_list,
            suggested_items = potential_items,
            all_potential_sets = ALL_POTENTIAL_SETS,
            which_run = "else statement")

    """ Debug this first -- not totally working (or is this only b/c I haven't added several iterations? """
    """ Test this by selecting everything on the first iteration, all sets should go to 100 """
    """ But we need to pass in ALL the sets in updated_sets, not just the matching sets """        
    """ Because otherwise it won't move any new sets past the cutoff point"""
    """ Dammit! That means we need to change getting the potential items -- to get ALL the items and not just the ones in matching sets"""
            # ---> So that means we'll need to filter the potential items
            # ---> To only those that would bump you over the cutoff


    """ Make it possible to do this through several iterations """
    """ Add a way to clear the additions and return to original combinations result page """















# App starts running here
if __name__ == "__main__":
    app.run(debug = True)







