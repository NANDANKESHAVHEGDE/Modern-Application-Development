from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.models import User, List, Card
from application.database import db
from flask import current_app as app
from flask_login import current_user
from datetime import datetime
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
import matplotlib.pyplot as plt
from flask import send_file
from application import tasks
import os
#from time import perf_counter_ns
from application.cache import cache, get_user_lists, delete_cache_list, get_user_cards, delete_cache_card

list_resource_fields = {
    'list_id': fields.Integer,
    'list_name': fields.String,
    'list_desc': fields.String,
    'username': fields.String
}

card_resource_fields = {
    'card_id' : fields.Integer,
    'card_name' : fields.String,
    'card_content' : fields.String,
    'card_deadline' : fields.String,
    'completion' : fields.String,
    'comp_date' : fields.String,
    'created_date' : fields.String,
    'updated_date' : fields.String,
    'list_id' : fields.Integer
}

create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('list_id')
create_list_parser.add_argument('list_name')
create_list_parser.add_argument('list_desc')
create_list_parser.add_argument('username')

update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('list_id')
update_list_parser.add_argument('list_name')
update_list_parser.add_argument('list_desc')
update_list_parser.add_argument('username')

create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('card_id')
create_card_parser.add_argument('card_name')
create_card_parser.add_argument('card_content')
create_card_parser.add_argument('card_deadline')
create_card_parser.add_argument('completion')
create_card_parser.add_argument('comp_date')
create_card_parser.add_argument('created_date')
create_card_parser.add_argument('updated_date')
create_card_parser.add_argument('list_id')

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('card_id')
update_card_parser.add_argument('card_name')
update_card_parser.add_argument('card_content')
update_card_parser.add_argument('card_deadline')
update_card_parser.add_argument('completion')
update_card_parser.add_argument('comp_date')
create_card_parser.add_argument('created_date')
create_card_parser.add_argument('updated_date')
update_card_parser.add_argument('list_id')


class CardAPI(Resource):
    @auth_required("token")    
    def get(self, username):
        flat_cards_arr = get_user_cards(username) 
        return marshal(flat_cards_arr, card_resource_fields)

    @auth_required("token")
    def post(self,username, list_id):
        delete_cache_card(username)
        args = create_card_parser.parse_args()   
        card_name = args.get("card_name")
        card_content = args.get("card_content")
        card_deadline = args.get("card_deadline")
        completion = args.get("completion")
        comp_date = args.get("comp_date")
        now = datetime.now()
        created_date = now.strftime("%Y-%m-%d")
        new_card = Card(card_name=card_name, card_content=card_content,card_deadline=card_deadline,completion=completion,comp_date=comp_date, list_id=list_id, created_date=created_date) 
        print(new_card)
        db.session.add(new_card)
        db.session.commit()
        return marshal(new_card, card_resource_fields)

    @auth_required("token")
    def delete(self,username, list_id,card_id):
        delete_cache_card(username)
        the_card = Card.query.filter_by(card_id=card_id).first()
        db.session.delete(the_card)
        db.session.commit()
        return "", 200

    @auth_required("token")
    def patch(self,username, list_id,card_id):
        delete_cache_card(username)
        print(list_id)
        print(card_id)
        print(username)
        args = update_card_parser.parse_args()
        the_card = Card.query.filter_by(card_id=card_id).first()
        print(the_card)
        the_card.list_id = args.get("list_id")
        the_card.card_name = args.get("card_name")
        the_card.card_content = args.get("card_content")
        the_card.card_deadline = args.get("card_deadline")
        the_card.completion = args.get("completion")
        now = datetime.now()
        the_card.updated_date = now.strftime("%Y-%m-%d")
        if the_card.completion == "yes":
            the_card.comp_date = now.strftime("%Y-%m-%d")
        elif the_card.completion == "no":
            the_card.comp_date = "null"   

        db.session.commit()
        return "", 200

class ListAPI(Resource):
    @auth_required("token")  
    def get(self, username):
        one_user_lists = get_user_lists(username)
        return marshal(one_user_lists, list_resource_fields)

    @auth_required("token")
    def post(self, username):
        delete_cache_list(username)
        args = create_list_parser.parse_args()
        list_name = args.get("list_name")
        list_desc = args.get("list_desc")
        new_list = List(list_name=list_name, list_desc=list_desc, username=username)
        print(new_list)
        db.session.add(new_list)
        db.session.commit()
        return marshal(new_list, list_resource_fields)

    @auth_required("token")
    def delete(self, username, list_id):
        delete_cache_list(username)
        the_list = List.query.filter_by(list_id=list_id).first()
        print(the_list)
        db.session.delete(the_list)
        db.session.commit()
        return "", 200

    @auth_required("token")
    def patch(self, username, list_id):
        delete_cache_list(username)
        print(username)
        print(list_id)
        args = update_list_parser.parse_args()
        the_list = List.query.filter_by(list_id=list_id).first()
        print(the_list)
        the_list.list_name = args.get("list_name")
        the_list.list_desc = args.get("list_desc")
        db.session.commit()
        return "", 200

class TimelineAPI(Resource):
    @auth_required("token")
    def get(self, username):
        try:
            os.remove("static/timeline.png")
        except:
            pass
        card_date = {}
        card_date_sort = {}
        tot_card_count = 0
        comp_card_count = 0
        lists = List.query.filter_by(username=username)
        for list in lists:
            cards = Card.query.filter_by(list_id = list.list_id)
            for card in cards:
                tot_card_count += 1
                if card.completion == "yes":
                    comp_card_count += 1
                    if card.comp_date in card_date.keys():
                        card_date[card.comp_date] = card_date[card.comp_date] + 1
                    else:
                        card_date[card.comp_date] = 1

        incomp_card_count = tot_card_count - comp_card_count
        card_date_sort = dict(sorted(card_date.items()))

        if tot_card_count != 0:
            plt.locator_params(axis='y', integer=True)
            plt.bar(card_date_sort.keys(),card_date_sort.values(), width=0.4)
            plt.xlabel('Dates')
            plt.ylabel('No of cards completed')
            plt.title("Timeline of card completion")
            plt.savefig('static/timeline.png')
            plt.clf()
            
        print("Is the graph ready?")    
        return send_file('static/timeline.png')

class CompstatAPI(Resource):
    @auth_required("token")    
    def get(self, username):
        try:
            os.remove("static/comp_stat.png")
        except:
            pass
        card_date = {}
        card_date_sort = {}
        tot_card_count = 0
        comp_card_count = 0
        lists = List.query.filter_by(username=username)
        for list in lists:
            print(type(list))
            cards = Card.query.filter_by(list_id = list.list_id)
            for card in cards:
                tot_card_count += 1
                if card.completion == "yes":
                    comp_card_count += 1
                    if card.comp_date in card_date.keys():
                        card_date[card.comp_date] = card_date[card.comp_date] + 1
                    else:
                        card_date[card.comp_date] = 1

        incomp_card_count = tot_card_count - comp_card_count
        card_date_sort = dict(sorted(card_date.items()))

        comp_status = [comp_card_count,incomp_card_count]
        card_labels = ["Completed - " + str(comp_card_count),"Incomplete - " + str(incomp_card_count)]

        if tot_card_count != 0:
            plt.title("Division of card completion")
            plt.pie(comp_status,labels = card_labels)
            plt.savefig('static/comp_stat.png')
            plt.clf()

        print("Is the second graph ready?")    
        return send_file('static/comp_stat.png')

class ExportAPI(Resource):
    def get(self, username):
        job = tasks.csv_export.delay(username)
        return str(job), 200        

class ListexportAPI(Resource):
    def get(self, username, list_id):
        job = tasks.csv_list_export.delay(username, list_id)
        return str(job), 200            


class SummaryAPI(Resource):
    @auth_required("token")  
    def get(self, username):
        summary_list = []
        one_user_lists = get_user_lists(username) 
        now = datetime.now()
        today = now.strftime("%Y-%m-%d") 
        for list in one_user_lists:
            card_list = []
            cards = Card.query.filter_by(list_id = list.list_id)  
            incomplete_count = 0
            deadline_crossed = 0
            complete_count = 0
            for card in cards:
                if card.completion == "no":
                    incomplete_count += 1
                else: 
                    complete_count += 1

                if card.card_deadline < today:
                    deadline_crossed += 1    
            
            card_list.extend([list.list_id,list.list_name,complete_count,incomplete_count,deadline_crossed])
            summary_list.append(card_list)

        return summary_list
