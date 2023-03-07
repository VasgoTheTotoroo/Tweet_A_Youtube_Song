from requests_oauthlib import OAuth1

GOOGLE_API_KEY = ''

TWITTER_AUTH = {
    "OAUTH_TOKEN": "",
    "OAUTH_SECRET": "",
    "CONSUMER_KEY": "",
    "CONSUMER_SECRET": "",
}

twitterOAuth = OAuth1(TWITTER_AUTH["CONSUMER_KEY"],
  client_secret=TWITTER_AUTH["CONSUMER_SECRET"],
  resource_owner_key=TWITTER_AUTH["OAUTH_TOKEN"],
  resource_owner_secret=TWITTER_AUTH["OAUTH_SECRET"])