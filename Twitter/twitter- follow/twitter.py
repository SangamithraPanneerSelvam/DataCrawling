import requests
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import tweepy


class DunBradstreet:
    def __init__(self):

        self.url1 = f"https://www.dnb.com/business-directory/top-results.html?term=enway%20gmbh&page=1"

    def selenium(self, url):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            executable_path=r"C://Users//Sangamithra//Desktop//twitter//geckodriver.exe",
            options=options,
        )
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.close()
        # html = BeautifulSoup(html)
        return html

    def selection(self):
        company = []
        tweets = []
        likes = []
        # assign the values accordingly
        consumer_key = "WvEH0XApBKa87rdvPWfCxxnLC"
        consumer_secret = "m6Kg0PmNUoFouOAwP37Ez5w0IoiuYfoj4vj1CVL1Lh8Qxrl5Of"
        access_token = "1465603561547612168-btnKPVkHzEJ4O1WPNh1M3dWB5zhYsD"
        access_token_secret = "WD8WCFat2R2eXU4W0jbyV5yZEvShg3nwteE3ZwyMMLrAM"

        # authorization of consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # set access to user's access key and access secret
        auth.set_access_token(access_token, access_token_secret)

        # calling the api
        api = tweepy.API(auth)

        topics_url = list(
            pd.read_excel(r"C://Users//Sangamithra//Desktop//twitter//bigpicture.xlsx")[
                "twitter_handle"
            ]
        )
        for topic in topics_url:
            company.append(topic)
            print(topic)
            if topic == "Nan":
                tweets.append("Nan")
                likes.append("Nan")
            else:

                self.url1 = f"https://twitter.com/{topic}/likes"
                info = self.parse(self.url1)
                print(info)
                tweets.append(info)
                screen_name = f"{topic}"
                # fetching the user
                try:
                    user = api.get_user(screen_name=screen_name)

                    favourites_count = user.favourites_count
                    print(favourites_count)
                    likes.append(favourites_count)
                except:
                    likes.append("Nan")

                # self.url2 = f"https://twitter.com/{topic}/likes"
                # like = self.parse_2(self.url2)
                # print(like)
                # likes.append(like)

        data_df = pd.DataFrame(
            {"twitter_handle": company, "Tweets": tweets, "Likes": likes}
        )
        data_df.to_csv(r"C://Users//Sangamithra//Desktop//twitter//tweet_counts.csv")

    def twitter(self):
        # assign the values accordingly
        consumer_key = "WvEH0XApBKa87rdvPWfCxxnLC"
        consumer_secret = "m6Kg0PmNUoFouOAwP37Ez5w0IoiuYfoj4vj1CVL1Lh8Qxrl5Of"
        access_token = "1465603561547612168-btnKPVkHzEJ4O1WPNh1M3dWB5zhYsD"
        access_token_secret = "WD8WCFat2R2eXU4W0jbyV5yZEvShg3nwteE3ZwyMMLrAM"

        # authorization of consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # set access to user's access key and access secret
        auth.set_access_token(access_token, access_token_secret)

        # calling the api
        api = tweepy.API(auth)

        # the ID of the user
        id = 57741058
        screen_name = "linderade"
        # fetching the user
        user = api.get_user(screen_name=screen_name)

        # fetching the favourites_count attribute
        favourites_count = user.favourites_count
        print(favourites_count)

    def parse(self, comp_url):

        dict = {}

        soup = self.selenium(comp_url)

        response = Selector(text=soup)

        dict = response.xpath('//div[@class="css-1dbjc4n r-1habvwh"]/div/text()').get()

        return dict

    def tweety(self):
        import requests

        # url = "https://twitter.com/login"
        url = "https://twitter.com/linderade/likes"
        payload = {
            "session[username_or_email]": "smithra06",
            "session[password]": "Octoberprincess",
        }
        response = requests.post(url, data=payload)
        response.json()


if __name__ == "__main__":
    obj = DunBradstreet()
    # obj.extract()
    obj.selection()
    # obj.twitter()
    # obj.tweety()
