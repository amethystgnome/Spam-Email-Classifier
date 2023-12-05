from flask import Flask, render_template, request, redirect
from mongoengine import Document, StringField, connect
import joblib
import spam_classifier
import logging

app = Flask(__name__)

model = None
vectorizer = None

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    subject = StringField(required=True)
    content = StringField(required=True)
    spam_or_real = StringField()

@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    if request.method == 'POST':
        spam_classifier.train()
        global model, vectorizer
        model = joblib.load('model.pkl')
        vectorizer = joblib.load('feature_extraction.pkl')
        return "Model retrained successfully", 200
    return render_template('train-model.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    global model, vectorizer
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        full_email = "subject: " + subject + "." + content
        if model and vectorizer:
            input_data_features = vectorizer.transform([full_email])
            prediction = model.predict(input_data_features)
            spam_or_real = "Spam" if prediction[0] == 0 else "Real"
        else:
            spam_or_real = "Error"

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





