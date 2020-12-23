import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
from sklearn.externals import joblib
from sqlalchemy import create_engine
import nltk
nltk.download(['punkt', 'wordnet'])
from nltk.corpus import stopwords


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('Disaster-Response', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
     # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    
    # Count and Percent of Messages by Genre
    gen_count = df.groupby('genre').count()['message']
    gen_per = round(100*gen_count/gen_count.sum(), 2)
    gen = list(gen_count.index)
    
    # Number of message per category
    cat_num = df.drop(['id', 'message', 'original', 'genre'], axis = 1).sum()
    cat_num = cat_num.sort_values(ascending = False)
    cat = list(cat_num.index)
    
    #Most used words
    mst_usd_word = pd.Series(' '.join(df['message']).lower().split())
    top_10_usd_word = mst_usd_word[~mst_usd_word.isin(stopwords.words("english"))].value_counts()[:10]
    list_top_10_usd_word = list(top_10_usd_word.index)

    
    # create visuals
    
    # First visual Pie chart showing the Count and Percent of Messages by Genre (modification of the original bar chart)
    graphs = [
        {
            "data": [
              {
                "type": "pie",
                "hole": 0.9,
                "name": "Genre",
                "pull": 0,
                "domain": {
                  "x": gen_per,
                  "y": gen
                },
                "marker": {
                  "colors": [
                    "#283B75",
                    "#9EB4F7",
                    "#537CF5"
                   ]
                },
                "textinfo": "label+value",
                "hoverinfo": "all",
                "labels": gen,
                "values": gen_count
              }
            ],
            "layout": {
              "title": "Count and Percent of Messages by Genre"
            }
        },
          
            # Second visual showing the Count of Messages by Category (bar chart)

        {
            "data": [
              {
                "type": "bar",
                "x": cat,
                "y": cat_num,
                "marker": {
                  "color": 'cadetblue'}
                }
            ],
            "layout": {
              "title": "Count of Messages by Category",
              'yaxis': {
                  'title': "Count"
              },
              'xaxis': {
                  'title': "Genre"
              },
              'barmode': 'group'
            }
        },
        
           # Third visual showing the Most Frequent Words used (bar chart)

          {
                'data': [
                    {
                        "type": "bar",
                        "x": list_top_10_usd_word,
                        "y": top_10_usd_word,
                        "marker": {
                          "color": 'darkcyan'}
                        }
                ],

                'layout': {
                    'title': 'Most Used Words',
                    'yaxis': {
                        'title': "Count"
                    },
                    'xaxis': {
                        'title': "Words"
                    }
                }
            }
        
        
        
    ]

    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()