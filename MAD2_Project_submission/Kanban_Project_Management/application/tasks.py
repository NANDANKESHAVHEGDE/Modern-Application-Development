from application.workers import celery
from datetime import datetime
from application.models import User,List,Card
from .database import db
from flask import current_app as app
from application.reportcreation import generate_report
from application.mailfunc import mail_report, mail_csv, mail_daily
import os
from celery.schedules import crontab

@celery.task()
def just_say_hello():
    print("INSIDE TASK")
    print("Hello noob")


@celery.task()
def monthly_report_generator():
    users = User.query.all()
    for user in users:
        username = user.username
        email = user.email
        today_date = datetime.now().strftime("%Y-%m-%d")
        the_user =  User.query.filter_by(username=username).first()
        lists = the_user.lists
        list_counter = 0
        cards_arr = []
        for list in lists: 
            list_counter += 1
            cards_arr.append(list.cards)

        completed_cards = 0
        total_cards = 0
        deadline_crossed = 0

        completed_cards_arr = []
        pending_cards_arr =[]
        flat_cards_arr =[]

        for sublist in cards_arr:
            for item in sublist:
                flat_cards_arr.append(item) 
        print(flat_cards_arr)

        for card in flat_cards_arr:
            total_cards += 1
            if card.completion == "yes":
                completed_cards += 1   
                completed_cards_arr.append(card) 
            elif card.completion == "no":   
                pending_cards_arr.append(card) 
                if card.card_deadline < today_date:
                    deadline_crossed += 1

        incomplete_cards = total_cards - completed_cards


        generate_report(username, lists, list_counter, completed_cards, total_cards, incomplete_cards, deadline_crossed, completed_cards_arr, pending_cards_arr, today_date)
        filename="{}_monthly_report_{}".format(username,today_date)
        mail_report(email,username,filename)

@celery.task()
def csv_export(username="newuser"):
    the_user = User.query.filter_by(username=username).first()
    user_lists = the_user.lists
    email = the_user.email

    try:
        os.remove("exported/{}.csv".format(username))
    except:
        pass

    if len(user_lists) > 0:
        lines = []
        lines.append("List ID,List Name,List Description\n")
        for list in user_lists:
            list_name = list.list_name
            list_id = list.list_id
            list_description = list.list_desc
            lines.append("{},{},{}\n".format(list_id,list_name,list_description))
        with open("exported/{}.csv".format(username), 'a+') as f:
            for line in lines:
                f.write(line)        
        filename="{}".format(username)
        mail_csv(email, username, filename)

@celery.task()
def csv_list_export(username, list_id):
    the_user = User.query.filter_by(username=username).first()
    email = the_user.email
    the_list = List.query.filter_by(list_id=list_id).first()
    cards = the_list.cards
    list_name = the_list.list_name

    try:
        os.remove("exported/{}_{}.csv".format(list_id,list_name))
    except:
        pass    

    if len(cards) > 0:
        lines = []
        lines.append("Card ID,Name,Content,Deadline,Completed,Completed On,Created On,Last updated\n")
        for card in cards:
            card_id = card.card_id
            card_name = card.card_name
            card_content = card.card_content
            card_deadline = card.card_deadline
            completion = card.completion
            comp_date = card.comp_date
            created_date = card.created_date
            updated_date = card.updated_date
            list_id = list_id
            lines.append("{},{},{},{},{},{},{},{}\n".format(card_id,card_name,card_content,card_deadline,completion,comp_date,created_date,updated_date))
        with open("exported/{}_{}.csv".format(list_id,list_name), 'a+') as f:
            for line in lines:
                f.write(line)        
        filename="{}_{}".format(list_id,list_name)
        mail_csv(email, username, filename)    

@celery.task()
def daily_reminder():
    users = User.query.all()
    for user in users:
        username = user.username
        email = user.email
        today_date = datetime.now().strftime("%Y-%m-%d")
        the_user =  User.query.filter_by(username=username).first()
        lists = the_user.lists
        list_counter = 0
        cards_arr = []
        for list in lists: 
            list_counter += 1
            cards_arr.append(list.cards)

        completed_cards = 0
        total_cards = 0

        completed_cards_arr = []
        flat_cards_arr =[]

        for sublist in cards_arr:
            for item in sublist:
                flat_cards_arr.append(item) 
        print(flat_cards_arr)

        for card in flat_cards_arr:
            total_cards += 1
            if card.completion == "yes":
                completed_cards += 1   

        incomplete_cards = total_cards - completed_cards

        if incomplete_cards != 0:
            mail_daily(email,username)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        #crontab(hour=13, minute=28),
        crontab(hour=0, minute=0, day_of_month=1),
        monthly_report_generator.s(),
        name = "Monthly Report dispatch"
    )       

@celery.on_after_configure.connect
def setup_periodic_tasks2(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=00),
        daily_reminder.s(),
        name = "Daily Reminder"
    )   