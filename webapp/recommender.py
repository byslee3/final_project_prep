from flask import Flask, render_template, redirect, request, session, flash
import engine


# Initialize app. Boilerplate to make it run
app = Flask(__name__)
app.config.from_object(__name__)


#############################
######## Functions ##########
#############################

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():

    starting_inventory = engine.get_starting_items()
    name = request.form['user_name']

    return render_template("inventory.html", starting_inventory=starting_inventory, name=name)


@app.route("/combinations", methods=["GET", "POST"])
def combinations():

    """
    -----> Having trouble with getting the input from the checkboxes
    for item in starting_inventory:
      if request.form['box'] == 1:
          selected_inventory.append(item)
    -----> How to implement??
    """

    selected_inventory = ["temp1", "temp2", "temp3", "temp4", "temp5"]

    # Get a list of set objects that match
    result = engine.return_matching_sets(selected_inventory)

    # Pull out the set URLs from the set objects (need to implement)
    existing_sets = result  # This will be an attribute in the future

    # Pull out the suggested items from the set objects (need to implement)
    suggested_items = result  # This will be an attribute in the future

    return render_template("combinations.html", selected_inventory=selected_inventory, existing_sets=existing_sets, suggested_items=suggested_items)


@app.route("/update_combinations", methods=["GET", "POST"])
def update_combinations():

    """ ?????????????? """
    existing_sets = "x"  # -----> How to grab this from the previous template?
    new_item = "x"  # -----> How to grab this from the previous template?

    updated_result = engine.return_updated_sets(existing_sets, new_item)

    """ Should be able to pull these out from the updated_result list"""
    selected_inventory = ["temp1", "temp2", "temp3", "temp4", "temp5"]
    suggested_items = ["itemA", "itemB", "itemC"]

    return render_template("combinations.html", selected_inventory=selected_inventory, existing_sets=existing_sets, suggested_items=suggested_items)














# App starts running here
if __name__ == "__main__":
    app.run(debug = True)







