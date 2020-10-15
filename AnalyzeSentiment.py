import re

import tweepy
import constant
from textblob import TextBlob

auth = tweepy.OAuthHandler(constant.consumer_key, constant.consumer_secret)
auth.set_access_token(constant.access_token, constant.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

keyword = "omnibuslaw"
hasilSearch = api.search(q=keyword, lang="en", count=100, tweet_mode='extended')

hasilAnalyze = []
for tweet in hasilSearch:
    tweet_properties = {
        'tanggal': tweet.created_at,
        'pengguna': tweet.user.screen_name,
        'tweet': tweet.full_text}
    tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())

    analyze = TextBlob(tweet_bersih)
    # try:
    #     analyze.translate(to="en")
    # except Exception as e:
    #     print(e)

    if analyze.sentiment.polarity > 0:
        tweet_properties["sentimen"] = "positif"
    elif analyze.sentiment.polarity == 0.0:
        tweet_properties["sentimen"] = "netral"
    else:
        tweet_properties["sentimen"] = "negatif"

    if tweet.retweet_count > 0:
        if tweet_properties not in hasilAnalyze:
            hasilAnalyze.append(tweet_properties)
    else:
        hasilAnalyze.append(tweet_properties)

tweet_positif = [t for t in hasilAnalyze if t["sentimen"] == "positif"]
tweet_netral = [t for t in hasilAnalyze if t["sentimen"] == "netral"]
tweet_negatif = [t for t in hasilAnalyze if t["sentimen"] == "negatif"]

print("Hasil sentimen")
print("positif : ", len(tweet_positif), ("({} %)".format(100 * len(tweet_positif) / len(hasilAnalyze))))
print("netral : ", len(tweet_netral), ("({} %)".format(100 * len(tweet_netral) / len(hasilAnalyze))))
print("negatif : ", len(tweet_negatif), ("({} %)".format(100 * len(tweet_negatif) / len(hasilAnalyze))))

print("========== Sentimen Positif ==========")
print(tweet_positif)
print("========== Sentimen Netral ==========")
print(tweet_netral)
print("========== Sentimen Negatif ==========")
print(tweet_negatif)
