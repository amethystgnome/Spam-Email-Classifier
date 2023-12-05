from flask import Flask, render_template, request, redirect
from mongoengine import Document, StringField, connect
import joblib
import spam_classifier
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

# Connects our db to a server 
connect('emails', host='localhost', port=27017)

# Creates schema for database
class Email(Document):
    subject = StringField(required=True)
    content = StringField(required=True)
    spam_or_real = StringField()

# Function to load model and vectorizer
def load_model_and_vectorizer():
    try:
        model = joblib.load('model.pkl')
        vectorizer = joblib.load('feature_extraction.pkl')
        return model, vectorizer
    except FileNotFoundError:
        print("Model or vectorizer files not found. Ensure they are in the correct directory.")
        return None, None

model, vectorizer = load_model_and_vectorizer()

"""@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    if request.method == 'POST':

        spam_classifier.train()
         After retraining, reload the model and vectorizer
        global model, vectorizer
        model, vectorizer = load_model_and_vectorizer()
        return "Model retrained successfully", 200
    return render_template('train-model.html')"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        logging.debug(f"Raw input received - Subject: {subject}, Content: {content}")
        full_email = "subject: " + subject + "." + content
        logging.debug(f"Formatted input for model - Full email: {full_email}")

        if model and vectorizer:
            input_data_features = vectorizer.transform([full_email])
            prediction = model.predict(input_data_features)
            logging.debug(f"Model input features: {input_data_features}")
            logging.debug(f"Model prediction: {prediction}")
            spam_or_real = "Spam" if prediction[0] == 0 else "Real"
        else:
            spam_or_real = "Error"
            logging.error("Model or vectorizer not loaded properly.")

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





