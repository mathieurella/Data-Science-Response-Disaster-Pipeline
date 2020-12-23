# Disaster Response Pipeline Project

## Project Overview

In this project, I'm applying data Engineering skills to analyze disaster data from Figure Eight to build a model for an API that classifies disaster messages.
Showing my ability to create basic data pipelines and write clean, organized code!

In the Project Workspace, you'll find a data set containing real messages that were sent during disaster events, ETL ET ML pipeline preparation to categorize these events so that we can send the messages to an appropriate disaster relief agency, and the web app.

This project include a web app where an emergency worker can input a new message and get classification results in several categories, it'll also display visualizations of the data.

## Project Components
This project has three main components.

####  1. ETL Pipeline Preparation
The ETL script does the following:

- Load messages and categories datasets
- Merge and clean the data
- Save the cleaned data in a SQLite database

####  2. ML Pipeline Preparation
The ML script does the following:

- Loads data from the SQLite database
- Splits the dataset into training and test sets
- Builds a text processing and machine learning pipeline
- Trains and tunes a model using GridSearchCV
- Outputs results on the test set
- Exports the final model as a pickle file

####  3. The Web App
The Web App is a condensed application of the Pipeline preparation work using flask, html, css and javascript

## Run The Web App Locally

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
