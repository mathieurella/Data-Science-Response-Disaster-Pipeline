import sys
# import libraries
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    ''' Load dataset & merge them on ID '''
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, how="left", on="id")

    return df


def clean_data(df):
    '''1/ Create a dataframe of the 36 individual category columns
       2/ Select the first row of the categories dataframe
       3/ Extract a list of new column names for categories & strip the last 2 characters
       4/ Rename the categories columns
       5/ Loop on each columns values to retrieve the the last character of the string
       6/ Loop to convert values column from string to numeric
       7/ Fit to get boolean
       8/ delete categories column from df
       9/ Concatenate message & categories
       10/ Drop duplicates of df      
    '''
    categories = df.categories.str.split(";",expand=True,)
    row = categories.iloc[0]
    category_colnames = row.str.split('-').str[0]
    categories.columns = category_colnames
    for column in categories:
        categories[column] = categories[column].str.strip().str[-1]
        categories[column] =  pd.to_numeric(categories[column], errors='coerce')    
    categories.related.replace(2,1,inplace=True) 
    del df['categories']
    df = pd.concat([df, categories], axis=1)
    df.drop_duplicates(inplace=True)
    
    return df

def save_data(df, database_filename):
    ''' Save into a Database '''
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('Disaster-Response', engine, index=False, if_exists = 'replace')

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()