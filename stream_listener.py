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
def fetch_tweets(user_id, seen_tweets, num_tweets):
    print(f"Fetching tweets for the user: {user_id}")
    if num_tweets > 100:
        print("Maximum number of tweets per request is 100. Setting num_tweets to 100.")
        num_tweets = 100
    
    try:
        # Fetch the most recent tweets with the limit set by num_tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=num_tweets,  # This will fetch up to num_tweets
            exclude='replies',       # Excludes replies
            tweet_fields=["created_at", "text", "author_id"]
        )
        
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
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")

# Get user ID from username
def get_user_id(username):
    print(f"Getting user ID for username: {username}")
    try:
        user = client.get_user(username=username)
        return user.data.id
    except Exception as e:
        raise ValueError(f"Failed to get user ID for username {username}: {str(e)}")

if not os.getenv('TESTING'):
    # Read username from command-line arguments
    if len(sys.argv) < 2:
        raise ValueError("Please provide the Twitter username as a command-line argument.")
    username = sys.argv[1]
    user_id = get_user_id(username)

    # Set to track seen tweets
    seen_tweets = set()

    # Main loop to periodically check for tweets every minute
    while True:
        fetch_tweets(user_id, seen_tweets, 5)
        time.sleep(60)  # Delay for 1 minute before fetching again
