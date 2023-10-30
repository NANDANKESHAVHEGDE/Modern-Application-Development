import smtplib
from email.message import EmailMessage

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "testemail@nandu.com"
SENDER_PASSWORD = ""

def mail_report(email,username,filename):
    msg = EmailMessage()
    msg['Subject'] = "Monthly Progress Report"
    msg["From"] = SENDER_ADDRESS
    msg["To"] = email
    top = "Hi {},\n\nPlease find your progress report for this month attached.".format(username)
    bottom = "Regards,\nKanban"
    full_body = top+"\n\n"+bottom
    msg.set_content(full_body)
    with open("exported/{}.pdf".format(filename),'rb') as f:
        report = f.read()
        name = f.name
    msg.add_attachment(report,filename=name,maintype='application',subtype='octet-stream')

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True        

def mail_csv(email, username, filename):    
    msg = EmailMessage()
    msg['Subject'] = "Exported CSV file"
    msg["From"] = SENDER_ADDRESS
    msg["To"] = email
    top = "Hi {},\n\nPlease find your exported CSV file attached.".format(username)
    bottom = "Regards,\nKanban"
    full_body = top+"\n\n"+bottom
    msg.set_content(full_body)
    with open("exported/{}.csv".format(filename),'rb') as f:
        report = f.read()
        name = f.name
    msg.add_attachment(report,filename=name,maintype='application',subtype='octet-stream')

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True    

def mail_daily(email,username):
    msg = EmailMessage()
    msg['Subject'] = "Daily Reminder"
    msg["From"] = SENDER_ADDRESS
    msg["To"] = email
    top = "Hi {},\n\nThis is a reminder to complete your pending tasks.".format(username)
    bottom = "Regards,\nKanban"
    full_body = top+"\n\n"+bottom
    msg.set_content(full_body)
    
    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True      