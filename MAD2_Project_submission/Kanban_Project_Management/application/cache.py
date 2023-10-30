from flask import current_app as app
from flask_caching import Cache
from application.models import User, List, Card
from application.database import db

cache = Cache(app)

@cache.memoize(50)   
def get_user_lists(username):
    one_user = User.query.filter_by(username=username).first()
    one_user_lists = one_user.lists
    return (one_user_lists)

def delete_cache_list(username):
    cache.delete_memoized(get_user_lists,username)    

@cache.memoize(50)   
def get_user_cards(username):
    the_user = User.query.filter_by(username=username).first()
    print(the_user)
    flat_cards_arr = []
    if the_user.lists != None:
        lists = the_user.lists
        cards_arr = []

        for list in lists:
            cards_arr.append(list.cards)

        for sublist in cards_arr:
            for item in sublist:
                flat_cards_arr.append(item) 
        print(flat_cards_arr)        
    return flat_cards_arr

def delete_cache_card(username):
    cache.delete_memoized(get_user_cards,username)      