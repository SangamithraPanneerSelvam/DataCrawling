from awena import Crawler
import re
import pandas as pd
import os


def AI_Glossary_merging():
    topics = list(
        pd.read_excel(
            r"C://Users//Sangamithra//Desktop//Data Crawling//201210_PLS KI-Landkarte_Anwendungen_Versand.xlsx"
        )["company"]
    )
    print(topics)
    new = [re.sub(r"_|\s+", " ", i).strip().lower() for i in topics]
    df = pd.DataFrame(list(set(new)), columns=["company"])
    df.to_csv(
        os.path.join(
            r"C://Users//Sangamithra//Desktop//Data Crawling", "Company_Names.csv"
        )
    )
    print("Comapny Names Successfully Crawled and Saved!")


class WikiDataCrawler:
    def __init__(self, index):
        self.index = index

    def search_terms(self):
        # topics = pd.read_csv(
        #     r"C://Users//Sangamithra//Desktop//Data Crawling//Company_Names.csv"
        # )
        topics = list(
            pd.read_excel(
                r"C://Users//Sangamithra//Desktop//Data Crawling//201210_PLS KI-Landkarte_Anwendungen_Versand.xlsx"
            )["company"]
        )

        return list(topics)

    def crawl(self):
        query_wiki = []
        data = []
        crawler = Crawler("en")  # set languge of labels and descriptions
        k = 0
        i = 0
        for query in self.search_terms():
            # print(query)

            k += 1
            #   print(k, query)
            qid = crawler.search(query)  # will return "Q937"
            #    print(qid)
            if re.search(r"Q\d+", str(qid)):
                i += 1
                query_wiki.append(query)
            info = crawler.load(qid)

            for key, value in info.items():
                if re.search(r"Q\d+", str(value)) and key != "id":
                    label = crawler.load(value)["label"]
                    info[key] = label
            print(info)
            data.append(info)
        print(data)
        data_df = pd.DataFrame(data)
        data_df.to_csv(r"C://Users//Sangamithra//Desktop//Data Crawling//WikiData.csv")

        # print(i)

        # df = pd.DataFrame(list(set(query_wiki)), columns=["company"])
        # df.to_csv(
        #     os.path.join(
        #         r"C://Users//Sangamithra//Desktop//Data Crawling",
        #         "Company_Wikidata.csv",
        #     )
        # )


#


if __name__ == "__main__":
    # AI_Glossary_merging()
    obj = WikiDataCrawler("wikidata")
    obj.crawl()
    # data = []
    # for doc in docs:
    #     data.append(doc["data"])
    # data_df = pd.DataFrame(data)
    # data_df.to_csv(r"C:\Users\Itisha Yadav\Desktop\FSTI\WikiData.csv")
