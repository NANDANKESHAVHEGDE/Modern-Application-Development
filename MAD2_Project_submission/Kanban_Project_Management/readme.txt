To run the app:
1. Install the requirements in the requirements.txt file
2. The main.py file is in the root folder. Run the command `python main.py` 
3. Use a browser to access the login page of the app which will be running on local host at port 8080 
4. To utilize Celery for some features, run the commands `sh local_workers.sh` and `sh.local_beat.sh`
5. Ensure Redis server is running. Install Redis to view cached files  
6. Set up mailhog and access it in the port as per config file of this app


# Folder Structure

- `db_directory` - has the sqlite DB
- `exported` - contains all the csv files and reports generated within the app
- `application` - contains the application code
- `static` - default `static` files folder. Contains all the styling and generated images
- `templates` - default flask templates folder


├── application
│   ├── __init__.py
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   ├── api.py
│   ├── cache.py
│   ├── mailfunc.py
│   ├── reportcreation.py
│   ├── tasks.py
│   ├── workers.py
│   └── __pycache__
|
├── db_directory
│   └── kanbanv23_db.sqlite3
|
├── exported
│   └── reports and csv files
├── static
│   ├── bootstrap
│   ├── application.js
│   ├── style.css
│   ├── style_form.css
│   └── style_login.css
|
├── templates
|   └── application.html
|    
├── local_beat.sh
├── local_workers.sh
├── main.py
├── monthly_report.html
├── readme.txt
└── requirements.txt

