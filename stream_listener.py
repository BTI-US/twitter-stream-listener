import tweepy
import sys
from dotenv import load_dotenv
import os
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Read the Bearer Token from environment variables
bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("Bearer Token is not set in the .env file.")

# Authentication with Twitter
client = tweepy.Client(bearer_token=bearer_token)

# Function to fetch and process tweets
def fetch_all_tweets(user_id, seen_tweets):
    print("Fetching tweets...")
    pagination_token = None
    while True:
        try:
            params = {
                "id": user_id,
                "max_results": 100,
                "exclude": 'replies',
                "tweet_fields": ["created_at", "text", "author_id"],
                "pagination_token": pagination_token
            }
            tweets = client.get_users_tweets(**params)
            if tweets.data:
                for tweet in tweets.data:
                    if tweet.id not in seen_tweets:
                        seen_tweets.add(tweet.id)  # Add new tweet ID to the set
                        # Format timestamp for file naming
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        filename = f"output/{tweet.author_id}_{tweet.id}_{timestamp}.md"
                        # Markdown content for the file
                        markdown_content = (
                            f"## Tweet by {tweet.author_id}\n\n"
                            f"**Tweet ID:** {tweet.id}\n"
                            f"**Created at:** {tweet.created_at}\n"
                            f"**Text:**\n\n"
                            f"{tweet.text}\n"
                        )
                        # Write to Markdown file
                        with open(filename, 'w', encoding='utf-8') as file:
                            file.write(markdown_content)
                        # Simple print to console
                        console_output = (
                            f"New tweet from {tweet.author_id}:\n"
                            f"Tweet ID: {tweet.id}\n"
                            f"Created at: {tweet.created_at}\n"
                            f"Text: {tweet.text}\n"
                        )
                        print(console_output)
            if 'next_token' in tweets.meta:
                pagination_token = tweets.meta['next_token']
            else:
                break
        except Exception as e:
            print(f"Error fetching tweets: {str(e)}")
            break

# Get user ID from username
def get_user_id(username):
    try:
        user = client.get_user(username=username)
        return user.data.id
    except Exception as e:
        raise ValueError(f"Failed to get user ID for username {username}: {str(e)}")

# Read username from command-line arguments
if len(sys.argv) < 2:
    raise ValueError("Please provide the Twitter username as a command-line argument.")
username = sys.argv[1]
user_id = get_user_id(username)

# Set to track seen tweets
seen_tweets = set()

# Main loop to periodically check for tweets every minute
while True:
    fetch_all_tweets(user_id, seen_tweets)
    time.sleep(60)  # Delay for 1 minute before fetching again
