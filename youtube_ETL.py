# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import googleapiclient.discovery
import pandas as pd
from datetime import datetime
import s3fs
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBnjtI9cIYpIGp7vvFHHUDR0EHKPHmRSrY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet, replies",
        videoId="q8q3OFFfY6c"
    )
    response = request.execute()
    comments_list = []
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId='q8q3OFFfY6c',
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    df = pd.DataFrame(comments_list)
    df.to_csv('s3://omar-sabor-first-test/youtube_comments.csv',index=False)


def process_comments(response_items):
    comments = []
    for comment in response_items:
            author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
            publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
            comment_info = {'author': author,
                    'comment': comment_text, 'published_at': publish_time}
            comments.append(comment_info)
    return comments
















