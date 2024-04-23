# Twitter Stream Listener

This project provides a real-time Twitter stream listener using the `tweepy` library and the Twitter API v2. It's designed to continuously monitor tweets from a specified user, printing new tweets to the console as they are posted.

## Prerequisites

Before you start, ensure you have the following:

- Python 3.6 or higher installed on your system.
- A Twitter Developer account and access to the Twitter API v2.
- A Bearer Token from your Twitter developer portal.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BTI-US/twitter-stream-listener.git
   cd twitter-stream-listener
   ```

2. **Install dependencies**:
   Install the required Python libraries using the following command:
   ```bash
   pip install tweepy python-dotenv
   ```

3. **Setup environment variables**:
   Create a `.env` file in the root directory of the project with the following content:
   ```plaintext
   BEARER_TOKEN=your_bearer_token_here
   ```
   Replace `your_bearer_token_here` with your actual Bearer Token.

## Configuration

The script uses command-line arguments to specify the user ID of the Twitter account to monitor. Ensure you have the numeric user ID of the Twitter account.

## Usage

To run the script, use the following command from the root directory of the project:

```bash
python stream_listener.py <user_id>
```

Replace `<user_id>` with the numeric user ID of the Twitter account you want to monitor.

## Features

- **Real-time Streaming**: Monitors tweets in real-time from a specified Twitter user.
- **Secure Authentication**: Uses environment variables to securely manage the Bearer Token.
- **Flexible**: Easily change the Twitter user you are monitoring by passing a different user ID as a command-line argument.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues if you have suggestions or encounter bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
