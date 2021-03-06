import sys
import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger', 'stopwords'])
import re
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import confusion_matrix,precision_recall_fscore_support,accuracy_score,label_ranking_average_precision_score,classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
import pickle
from sqlalchemy import create_engine
from sklearn.svm import SVC, LinearSVC
from sklearn.multiclass import OneVsRestClassifier


def load_data(database_filepath):
    ''' 1/ Read Disaster-Response table
        2/ Create X & Y
        3/ Retrieve category name from Y columns          
    '''
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('Disaster-Response', con=engine)
    X = df['message']
    Y = df.drop(['id', 'message', 'original', 'genre'], axis=1)
    category_names = Y.columns
    return X , Y , category_names


def tokenize(text):
    '''1/ Normalize case and remove punctuation
       2/ tokenize text
       3/ Lemmatize and remove stop words
    '''

    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens


def build_model():
    ''' building the model '''
    pipeline  = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(OneVsRestClassifier(LinearSVC(random_state=0))))
    ])
    
    parameters = {
    'vect__ngram_range': ((1, 1), (1, 2))
    }

    cv = GridSearchCV(pipeline, param_grid=parameters, n_jobs=4, verbose=2);
    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    ''' evaluate the model through classification report showing the : precision, recall, f1-score & support '''
    Y_pred = model.predict(X_test)

    for i in range(36):
        print(Y_test.columns[i], ':')
        print(classification_report(Y_test.iloc[:,i], Y_pred[:,i]), '------------------------------------------------------------------')


def save_model(model, model_filepath):
     ''' Save the model as a pickle file '''
     pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()