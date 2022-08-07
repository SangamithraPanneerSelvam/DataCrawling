import requests
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


class DunBradstreet:
    def __init__(self):
        self.url1 = ""
        self.data = []

    def extract(self):
        extract_company = list(
            pd.read_excel(
                r"C://Users//Sangamithra//Desktop//selenium//201210_PLS KI-Landkarte_Anwendungen_Versand.xlsx"
            )["company"]
        )

        new = [i.strip().lower() for i in extract_company]
        df = pd.DataFrame(list(set(new)), columns=["company"])
        df.to_csv(
            os.path.join(
                r"C://Users//Sangamithra//Desktop//selenium", "Company_Names.csv"
            )
        )

    def selenium(self, url):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            executable_path=r"C://Users//Sangamithra//Desktop//selenium//geckodriver-v0.30.0-win64//geckodriver.exe",
            options=options,
        )
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.close()
        # html = BeautifulSoup(html)
        return html

    def selection(self):

        topics = list(
            pd.read_excel(
                r"C://Users//Sangamithra//Desktop//selenium//Company_left.xlsx"
            )["company"]
        )
        for topic in topics:
            print(topic)

            if " " in topic:
                topic_url = topic.split()
                if len(topic_url) == 2:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}&page=1"
                elif len(topic_url) == 3:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}%20{topic_url[2]}&page=1"
                elif len(topic_url) == 4:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}%20{topic_url[2]}%20{topic_url[3]}&page=1"
                elif len(topic_url) == 5:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}%20{topic_url[2]}%20{topic_url[3]}%20{topic_url[4]}&page=1"
                elif len(topic_url) == 6:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}%20{topic_url[2]}%20{topic_url[3]}%20{topic_url[4]}%20{topic_url[5]}&page=1"
                elif len(topic_url) == 7:
                    self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic_url[0]}%20{topic_url[1]}%20{topic_url[2]}%20{topic_url[3]}%20{topic_url[4]}%20{topic_url[5]}%20{topic_url[6]}&page=1"
            else:
                self.url1 = f"https://www.dnb.com/business-directory/company-search.html?term={topic}&page=1"

            self.search_query(topic, url=self.url1)

        print(self.data)
        data_df = pd.DataFrame(self.data)
        data_df.to_csv(
            r"C://Users//Sangamithra//Desktop//selenium//company_profile_left.csv"
        )

    def search_query(self, topic, url):

        soup = self.selenium(url)
        response = Selector(text=soup)

        for info in response.xpath('//div[@class="primary_name"]/a'):
            company_name = info.xpath(".//text()").get()
            company_link = info.xpath(".//@href").get()
            name = str(company_name).lower()
            gmbh_name = topic + " " + "gmbh"

            if name == topic:
                print("After comparison ----->")
                print(name, "\n", company_link)

                comp_url = f"https://www.dnb.com{company_link}"
                #     print(comp_url)

                info = self.parse(comp_url)
                print(info)
                self.data.append(info)
                # return info
                # print("data appended")
            elif name == gmbh_name:

                print("After comparison ----->")
                print(name, "\n", company_link)

                comp_url = f"https://www.dnb.com{company_link}"
                #     print(comp_url)

                info = self.parse(comp_url)
                print(info)
                self.data.append(info)
                # return info
                # print("data appended")
            else:
                pass

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            print(next_page)
            self.search_query(topic, url=next_page)

    def parse(self, comp_url):

        dict = {}

        soup = self.selenium(comp_url)
        response = Selector(text=soup)
        dict["company_name"] = response.xpath(
            '//span[@name="company_name"]/span/text()'
        ).get()

        dict["company_description"] = response.xpath(
            '//span[@name="company_description"]/span/text()'
        ).get()
        dict["employees"] = response.xpath(
            '//span[@name="employees_this_site"]/span/text()'
        ).get()
        dict["revenue"] = response.xpath(
            '//span[@name="revenue_in_us_dollar"]/span/text()'
        ).get()
        dict["ESG"] = response.xpath('//span[@name="esgRank"]/span/text()').get()
        dict["ESG_avg_industry"] = response.xpath(
            '//span[@name="esgIndustryAverage"]/span/text()'
        ).get()

        return dict

        # else:


if __name__ == "__main__":
    obj = DunBradstreet()
    # obj.extract()
    obj.selection()
