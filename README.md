# Running Instructions
You must run both the frontend app and backend app for them to communicate.
Make sure that all dependencies are installed. The frontend dependencies are through node and npm. The backend dependencies are through the `requirements.txt` in the backend directory.

## Frontend
1. `cd` to the frontend directory
2. run `npm i` to install necessary Node/Angular packages
3. run `npm run start`
4. open localhost:4200 in browser

## Backend
NOTE: Do not remove or delete the database or migrations folder. The database has been created and seeded appropriately.
1. `cd` to the backend directory
2. run `pip3 install -r requirements.txt` to install dependencies 
3. on mac or linux, run `./flast-restart-on-file-change.sh`; on windows run `set FLASK_DEBUG=1 && set FLASK_APP=app.py && flask run`
If you want to see the current state of the database you can go to http://127.0.0.1:5000/list in your browser (or localhost:5000/list)

## Play around with Mapt!
You can create an account, add your trips, view other user's mapt (if they are public), and see statistics about your travel history!
