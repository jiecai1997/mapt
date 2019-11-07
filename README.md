# Backend

## Run Flask App (THIS SHOULD BE DONE FIRST bc app.db is up to date)
1. `$cd` to the backend folder
2. Install dependencies
3. `$flask run` or `./flast-restart-on-file-change.sh`
4. Open `http://127.0.0.1:5000/` in browser

## Remake the app.db
1. If models.py has been edited, cd to the backend folder
2. then run `flask db migrate`
3. then run `flask db upgrade`

## Populate the database with Airports and Airlines (ONLY DO IF YOU FUCKED SOMETHING up with app.db OR want to start over)
NOTE ALL COMMANDS SHOULD BE RUN IN the BACKEND DIRECTORY
1. If the database needs to be reset, run `flask db downgrade`
2. then run `flask db upgrade`
3. then run `python ./app/seed.py`
4. If you want to see the inserts with general data for testing run `python ./app/test_inserts.py`
5. To generate the files that are the outputs from the test queries run `python ./app/test-samples.py` and the outputs should be in the app/csv directory
