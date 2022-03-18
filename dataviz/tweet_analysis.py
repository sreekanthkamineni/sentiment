from textblob import TextBlob
import tweepy
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('api_key')
api_key_secret = os.getenv('api_key_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


def tweet_senti(query):

    auth_handeler = tweepy.OAuthHandler(consumer_key=api_key,
                                        consumer_secret=api_key_secret)
    auth_handeler.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handeler)

    tweeets = tweepy.Cursor(api.search_tweets, q=query, lang='en',
                            tweet_mode='extendad').items(1000)
    polarity = positive = negative = nutral = 0
    data_dict = {}
    try:
        for tweet in tweeets:
            final_text = tweet.text.replace('RT', '')
            if final_text.startswith(' @'):
                position = tweet.text.index(':')
                final_text = final_text[position:]
            analysis = TextBlob(final_text)
            polarity += analysis.polarity
            if analysis.polarity > 0:
                positive += 1
                try:
                    data_dict[str(tweet.created_at.date())][0] += 1
                except KeyError:
                    data_dict[str(tweet.created_at.date())] = [0, 0, 0]
                    data_dict[str(tweet.created_at.date())][0] += 1

            elif analysis.polarity < 0:
                negative += 1
                try:
                    data_dict[str(tweet.created_at.date())][1] += 1
                except KeyError:
                    data_dict[str(tweet.created_at.date())] = [0, 0, 0]
                    data_dict[str(tweet.created_at.date())][1] += 1
            else:
                nutral += 1
                try:
                    data_dict[str(tweet.created_at.date())][2] += 1
                except KeyError:
                    data_dict[str(tweet.created_at.date())] = [0, 0, 0]
                    data_dict[str(tweet.created_at.date())][2] += 1
    except tweepy.errors.TooManyRequests:
        print("twitter data exosted with requests")
        return data_dict
    return data_dict


if __name__ == '__main__':
    print(tweet_senti('modi'))
