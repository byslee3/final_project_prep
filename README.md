final_project_prep
==================

GUIDE TO FILES / FOLDER STRUCTURE

admin -- My own notes, not relevant  

archive -- Old versions of stuff, not relevant  

database -- Includes all files used to create SQL database from Polyvore API  

    polyvore.db -- Latest version of database. However all data will need to be re-pulled at future date as my data needs changed later in the project. Right now, web app is built on small sample of test data.  
    polvore.py -- Script for pulling JSON files from Polyvore and parsing it to get data that I need  
    model.py -- Script for entering data into SQL database  
    seed.py -- Script that calls on functions in polyvore.py and model.py, history of what I did to create database  
    
webapp -- Main files to make the webapp run  

    recommender.py -- Communicating between Python, Flask, and HTML templates. Run this to make webapp run.  
    engine2.py -- Holds all the functions to power recommender.py. Function to match sets, return suggested items, etc.  
    polyvore.db -- Test database used for building out first version of app. Needs to be updated later.  
    static -- Holds CSS files  
    templates -- Holds all HTML views  
    all other files -- Old versions, not relevant
