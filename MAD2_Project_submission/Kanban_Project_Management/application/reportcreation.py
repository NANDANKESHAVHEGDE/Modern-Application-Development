from jinja2 import Template
from weasyprint import HTML, CSS
import os, time

def generate_report(username, lists, list_counter, completed_cards, total_cards, incomplete_cards, deadline_crossed, completed_cards_arr, pending_cards_arr, today_date):
    with open('monthly_report.html') as file:
        template = Template(file.read())
    html = template.render(username=username,lists=lists,list_counter=list_counter,completed_cards=completed_cards,total_cards=total_cards,incomplete_cards=incomplete_cards,deadline_crossed=deadline_crossed,completed_cards_arr=completed_cards_arr,pending_cards_arr=pending_cards_arr,date=today_date)
    with open("exported/{}_monthly_report_{}.html".format(username,today_date),"w") as f:
        f.write(html)
    HTML("exported/{}_monthly_report_{}.html".format(username,today_date)).write_pdf("exported/{}_monthly_report_{}.pdf".format(username,today_date))    