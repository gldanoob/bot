import os
from dotenv import load_dotenv

import praw

load_dotenv()
ID = os.getenv("REDDIT_ID")
SECRET = os.getenv("REDDIT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(client_id=ID, client_secret=SECRET,
                     username=USERNAME, password=PASSWORD, user_agent='wut')


def random(sub):
    subreddit = reddit.subreddit(sub)
    post = subreddit.random()
    return post.title, post.selftext, post.url


