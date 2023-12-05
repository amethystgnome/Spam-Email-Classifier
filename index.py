from flask import Flask, render_template, request, redirect
from mongoengine import Document, StringField, connect
import joblib
import spam_classifier

app = Flask(__name__)

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    subject = StringField(required=True)
    content = StringField(required=True)
    spam_or_real = StringField()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        full_email = "subject: " + subject + "." + content
        spam_or_real = spam_classifier.prediction(full_email)

        # Save email details to database
        entry = Email(subject=subject, content=content, spam_or_real=spam_or_real)
        entry.save()
        
        return redirect('/')
    return render_template('index.html')

@app.route("/emails")
def print_emails():
    emails = Email.objects.all()
    return render_template('emails.html', emails=emails)

if __name__ == '__main__':
    app.run(debug=True)





