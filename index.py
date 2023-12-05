from flask import Flask, render_template, request, redirect
from mongoengine import Document, StringField, connect


app = Flask(__name__)

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    subject = StringField(required=True)
    content = StringField(required=True)
    spam_or_real = StringField()

# prints emails for test
for email in Email.objects:
    print(email.subject, email.content)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        entry = Email(subject= subject, content= content, spam_or_real = "True")
        entry.save()
        full_email = "subject:" + subject + "." + content
        # Handle the submitted data (save, send, process, etc.)
        # For now, just redirect to the home page
        return redirect('/')
    return render_template('index.html')


@app.route("/emails")
def print_emails():
    emails = Email.objects.all()

    return render_template('emails.html', emails=emails)
    





