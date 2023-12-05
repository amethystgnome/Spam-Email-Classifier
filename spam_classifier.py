#Description: Spam Email Classifier
#Authors: Aubrianna Sample and Dustin Chavez
#Input: Email Subject and Body
#Output: Boolean value, spam or not spam
#Model: MultinomialNB()
#Libraries Used: Sklearn (Machine Learning), Pandas, Joblib (Model and Feature Extraction Saving)
#Purpose: Takes an email subject and body as input, runs email through preprocessing, text analysis, and trained machine learning model
#and outputs boolean value of spam or real.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

def train():
  #Open dataset
  df = pd.read_csv('spam_ham_dataset.csv')

  """Data Preprocessing"""
  data = df.head(5)
  print(data)

  data = df.where((pd.notnull(df)), '')

  data.head(10)

  data.info()

  data.shape
  
  #Assign spam as 0 and ham(real) as 1.
  data.loc[data['label'] == 'spam', 'label'] = 0
  data.loc[data['label'] == 'ham', 'label'] = 1

  X = data['text']
  Y = data['label']
  """End data preprocessing"""
  
  #Split data
  X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size= 0.2, random_state = 3)
  
  """Feature extraction (vectorization, fitting/transforming)"""
  feature_extraction = TfidfVectorizer(min_df=2, max_df=0.5, stop_words='english',
                                      lowercase=True, ngram_range=(1, 2))
  X_train_features = feature_extraction.fit_transform(X_train)
  X_test_features = feature_extraction.transform(X_test)
  """End feature extraction"""
 
  #Put vectorization into file
  joblib.dump(feature_extraction, 'feature_extraction.pkl')


 

  #Check for NaN values and handle them
  if Y_train.isnull().values.any():
      Y_train = Y_train.fillna(0)
  if Y_test.isnull().values.any():
      Y_test = Y_test.fillna(0)

  #Now convert to integer type
  Y_train = Y_train.astype('int')
  Y_test = Y_test.astype('int')
  Y_train = Y_train.astype('int')
  Y_test = Y_test.astype('int')

  "Model training and fitting"
  model = MultinomialNB()
  model.fit(X_train_features, Y_train)
  joblib.dump(model, 'model.pkl')
  """End model training and fitting"""

  
  #The following are prediction and accuracy scores to check our model's accuracy and performance
  prediction_on_training_data = model.predict(X_train_features)
  accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)

  print('Accuracy on training data: ', accuracy_on_training_data)

  prediction_on_test_data = model.predict(X_test_features)
  accuracy_on_test_data = accuracy_score(Y_test, prediction_on_test_data)

  print('Accuracy on test data: ', accuracy_on_test_data)
