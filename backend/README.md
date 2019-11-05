# Backend

## Run Flask App
1. `$cd` to this folder
2. Install dependencies
3. `$flask run` or `./flast-restart-on-file-change.sh`
4. Open `http://127.0.0.1:5000/` in browser

## Remake the app.db
1. if models.py has been edited, cd to this folder
2. then run `flask db migrate`
3. then run `flask db upgrade`
