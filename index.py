from flask import Flask, render_template, request, redirect
from mongoengine import Document, StringField, connect
import joblib
import spam_classifier

app = Flask(__name__, template_folder = 'templates', static_folder = 'styles')

model = None
vectorizer = None

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    subject = StringField(required=True)
    content = StringField(required=True)
    spam_or_real = StringField()

def load_model_and_vectorizer():
    global model, vectorizer
    spam_classifier.train()  # Train the model
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('feature_extraction.pkl')

load_model_and_vectorizer()

@app.route('/', methods = ['GET', 'POST'])
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
        entry = Email(subject = subject, content = content, spam_or_real = spam_or_real)
        entry.save()
        
        return redirect('/emails')
    return render_template('index.html')

@app.route("/emails")
def print_emails():
    emails = Email.objects.all()
    return render_template('emails.html', emails = emails)

if __name__ == '__main__':
    app.run(debug = True)





