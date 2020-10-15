import csv
import re

import tweepy
import constant
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# cek daftar kata stopword
# factory = StopWordRemoverFactory()
# stop = factory.get_stop_words()
# print(stop)

auth = tweepy.OAuthHandler(constant.consumer_key, constant.consumer_secret)
auth.set_access_token(constant.access_token, constant.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# cari berdasarkan keyword
keyword = "@indihome"
max_tweet = 1000
# hasilUser = api.user_timeline(id=keyword, count=2)
hasilSearch = api.search(q=keyword, lang="id", count=1000, tweet_mode='extended')
header = ['keyword', 'tanggal', 'username', 'name', 'tweet', 'total retweet', 'total like', 'url ID', 'location',
          'source']
print("_____________ proses scraping data ______________")
with open('dataScrapek5.csv', 'w') as cs:
    w = csv.writer(cs)
    w.writerow(header)
    for tweet in hasilSearch:
        tweet_text = str(tweet.full_text)
        if tweet_text.startswith("RT @"):
            # CASE FOLDONG
            # hilangin tanda baca
            tweet_bersih_retweet = ' '.join(
                re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",
                       tweet.retweeted_status.full_text).split())
            # text ke lowercase
            tweet_lower_case = tweet_bersih_retweet.lower()

            # remove angka
            tweet_remove_angka = re.sub(r"\d+", "", tweet_lower_case)

            # TOKENIZING adalah proses pemisahan teks menjadi potongan-potongan yang disebut sebagai token
            # untuk kemudian di analisa
            tweet_token = word_tokenize(tweet_remove_angka)
            print(tweet_token)

            # FILTERING stopword removal Filtering adalah tahap mengambil kata-kata penting dari hasil token dengan
            # menggunakan algoritma stoplist (membuang kata kurang penting) atau wordlist (menyimpan kata penting).
            factory = StopWordRemoverFactory()
            stopword = factory.create_stop_word_remover()
            resultStopwords = stopword.remove(tweet_remove_angka)
            print(resultStopwords)

            # STEMMING adalah proses menghilangkan kata imbuhan kebentuk dasar
            factorys = StemmerFactory()
            stemmer = factorys.create_stemmer()
            resultStemmer = stemmer.stem(resultStopwords)
            print(resultStemmer)

            w.writerow((keyword,
                        tweet.created_at,
                        tweet.user.screen_name,
                        tweet.user.name,
                        tweet_token,
                        tweet.retweeted_status.retweet_count,
                        tweet.retweeted_status.favorite_count,
                        "https://twitter.com/twitter/statuses/" + tweet.id_str,
                        tweet.user.location,
                        tweet.source))

        else:
            tweet_bersih = ' '.join(
                re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())
            lower_case = tweet_bersih.lower()

            w.writerow((keyword,
                        tweet.created_at,
                        tweet.user.screen_name,
                        tweet.user.name,
                        lower_case,
                        tweet.retweet_count,
                        tweet.favorite_count,
                        "https://twitter.com/twitter/statuses/" + tweet.id_str,
                        tweet.user.location,
                        tweet.source))
