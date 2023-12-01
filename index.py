from flask import Flask, render_template
from mongoengine import Document, StringField, connect


app = Flask(__name__)

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    title = StringField(required=True)
    content = StringField(required=True)

# prints emails for test
for email in Email.objects:
    print(email.title, email.content)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/emails")
def print_emails():
    emails = Email.objects.all()

    return render_template('emails.html', emails=emails)
    


