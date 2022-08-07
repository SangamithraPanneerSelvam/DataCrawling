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

        self.url = r"https://www.dnb.com/business-directory/company-profiles.dalmer_consultancy.4022ceb19412e44b5bd7efd4e1d4570e.html"

        self.url1 = f"https://www.dnb.com/business-directory/top-results.html?term=enway%20gmbh&page=1"

        self.web = "https://duckduckgo.com/"

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
        data = []

        topics_url = list(
            pd.read_excel(
                r"C://Users//Sangamithra//Desktop//selenium//Company_left.xlsx"
            )["url"]
        )
        for topic in topics_url:

            print(topic)
            self.url1 = f"{topic}"
            info = self.parse(self.url1)
            print(info)
            data.append(info)

        print(data)

        data_df = pd.DataFrame(data)
        data_df.to_csv(r"C://Users//Sangamithra//Desktop//selenium//company.csv")

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
