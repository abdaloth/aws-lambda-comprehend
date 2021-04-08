import json

import boto3
import botocore

import pandas as pd
import requests
import boto3

def get_comments(queries):
    
    comments = []
    for query in queries:
        url = f"https://api.pushshift.io/reddit/search/comment/?q={query}&size=1"
        request = requests.get(url)
        json_response = request.json()['data'][0]
        comments.append(json_response['body'])
    df = pd.DataFrame({"queries": queries, "comments": comments})
    return df


def create_sentiment(row):
    """Uses AWS Comprehend to Create Sentiments on a DataFrame"""
    comprehend = boto3.client(service_name="comprehend")
    payload = comprehend.detect_sentiment(Text=row, LanguageCode="en")
    sentiment = payload["Sentiment"]
    return sentiment


def apply_sentiment(df, column="comments"):
    """Uses Pandas Apply to Create Sentiment Analysis"""

    df["Sentiment"] = df[column].apply(create_sentiment)
    return df
    
    
if __name__ == '__main__':
    df = get_comments(['summer', 'coffee', 'ps4'])
    df = apply_sentiment(df)
    print(df)