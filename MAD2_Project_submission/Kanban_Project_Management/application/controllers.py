from datetime import datetime
from flask import Flask, request
from flask import render_template
from flask import current_app as app
from application.models import User,List,Card
from .database import db
from datetime import datetime
from application import tasks
import matplotlib.pyplot as plt

@app.route("/", methods=["GET","POST"])
def home():
    return render_template('application.html')


@app.route("/hello/repgen", methods=["GET", "POST"])
def repgen():
    job = tasks.monthly_report_generator.delay()
    return str(job), 200





 
 

    


