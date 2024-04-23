from unittest.mock import Mock, patch, mock_open
from stream_listener import fetch_tweets, get_user_id
from freezegun import freeze_time

author_name = 'LotsoFandom'
author_id = '1742141344787857408'
tweet_id = '1777555856705667262'

# Test for get_user_id function
def test_get_user_id():
    with patch('stream_listener.client') as mocked_client:
        mocked_client.get_user.return_value = Mock(data=Mock(id=author_id))
        user_id = get_user_id(author_name)
        assert user_id == author_id
        mocked_client.get_user.assert_called_once_with(username=author_name)

# Test for fetch_tweets function
@freeze_time("2023-04-23 01:01:01")
def test_fetch_tweets():
    with patch('stream_listener.client') as mocked_client, \
         patch('builtins.open', mock_open(), create=True) as mocked_file:  # Note the create=True for broader patching
        # Setup the mock return value for tweets
        mocked_client.get_users_tweets.return_value = Mock(
            data=[Mock(id=tweet_id, author_id=author_id, created_at='2023-01-01', text='Sample Tweet')]
        )
        
        seen_tweets = set()

        # Action
        fetch_tweets(author_id, seen_tweets, 1)

        # Assert
        assert tweet_id in seen_tweets
        mocked_client.get_users_tweets.assert_called_once_with(
            id=author_id,
            max_results=1,
            exclude='replies',
            tweet_fields=["created_at", "text", "author_id"]
        )

        # Assert that the file was attempted to be opened with the correct parameters
        filename = f"output/{author_id}_{tweet_id}_20230423010101.md"
        mocked_file.assert_called_once_with(filename, 'w', encoding='utf-8')

        # Check the content written to the file
        mocked_file().write.assert_called_once_with(
            f"## Tweet by {author_id}\n\n"
            f"**Tweet ID:** {tweet_id}\n"
            "**Created at:** 2023-01-01\n"
            "**Text:**\n\n"
            "Sample Tweet\n"
        )

# Test for handling too many tweets requested
def test_fetch_tweets_too_many():
    with patch('stream_listener.client') as mocked_client:
        fetch_tweets(author_id, set(), 150)
        mocked_client.get_users_tweets.assert_called_with(
            id=author_id,
            max_results=100,
            exclude='replies',
            tweet_fields=["created_at", "text", "author_id"]
        )
