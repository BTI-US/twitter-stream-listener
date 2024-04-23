import tweepy
import sys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read the Bearer Token from environment variables
bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("Bearer Token is not set in the .env file.")

# Define the stream listener
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"New tweet from {tweet.author_id}: {tweet.text}")

# Read user ID from command-line arguments
if len(sys.argv) < 2:
    raise ValueError("Please provide the user ID as a command-line argument.")
user_id = sys.argv[1]

# Initialize the listener with the Bearer Token
listener = MyStreamListener(bearer_token=bearer_token)
listener.add_rules(tweepy.StreamRule(f"from:{user_id}"))
listener.filter(tweet_fields=["author_id", "text"])
