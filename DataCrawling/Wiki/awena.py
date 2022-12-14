import requests


class Crawler:
    VERSION = "0.1"
    USER_AGENT = (
        "Mozilla/5.0 (compatible; Awena/"
        + VERSION
        + "; +https://github.com/sedthh/awena-wikidata-crawler/)"
    )

    ##### CONSTRUCTOR #####
    def __init__(self, lang="en"):
        self.lang = lang.lower()
        self.cache = {}
        self.n = 0

    ##### DATA MODEL #####
    def __repr__(self):
        return "<Awena Search instance at {0}>".format(hex(id(self)))

    def __str__(self):
        return self.query

    def __len__(self):
        return len(self.cache)

    def __eq__(self, other):
        if isinstance(other, bool):
            return bool(self.cache) == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    ##### CLASS FUNCTIONS #####

    def number_of_requests(self):
        return self.n

    def search(self, query):
        return self._request(query, False)

    def load(self, id=None):
        if not id:
            return {}
        if id not in self.cache:
            data = self._request(False, id)
            self.cache[id] = self._parse(data, id)

        return self.cache[id]

    def _request(self, query=False, id=False):
        headers = {"User-Agent": Crawler.USER_AGENT}
        if id:
            params = {
                "action": "wbgetentities",
                "ids": id,
                "language": self.lang,
                "format": "json",
            }
        else:
            if not query:
                return None
            query = query.strip()
            params = {
                "action": "wbsearchentities",
                "search": query,
                "language": self.lang,
                "format": "json",
            }
        data = requests.get(
            "https://www.wikidata.org/w/api.php", headers=headers, params=params
        )
        result = data.json()

        self.n += 1
        if "error" in result:
            # raise Exception(result["error"]["code"], result["error"]["info"])
            pass
        elif query and "search" in result and result["search"]:
            guess = None
            for item in result["search"]:
                if (
                    "id" in item
                    and "match" in item
                    and "text" in item["match"]
                    and "language" in item["match"]
                ):
                    if item["match"]["language"] == self.lang:
                        if not guess:
                            guess = item["id"]
                        if item["match"]["text"].lower().strip() == query.lower():
                            return item["id"]
                return guess
        elif id and "entities" in result and result["entities"]:
            if id in result["entities"] and result["entities"][id]:
                return result["entities"][id]
        if query:
            return {}
        return None

    def _parse(self, data, id):
        result = {"id": id}
        if id and data:
            if "labels" in data:
                if self.lang in data["labels"]:
                    result["label"] = data["labels"][self.lang]["value"]
            if "descriptions" in data:
                if self.lang in data["descriptions"]:
                    result["description"] = data["descriptions"][self.lang]["value"]
            if "claims" in data:
                # results to human readable format
                for key in data["claims"]:
                    try:
                        if key == "P31":  # instance of
                            result["instance"] = data["claims"][key][0]["mainsnak"][
                                "datavalue"
                            ]["value"]["id"]
                        elif key == "P1128":  # Employee
                            result["employees"] = data["claims"][key][0]["mainsnak"][
                                "datavalue"
                            ]["value"]["amount"]
                        elif key == "P2139":  # Total Revenue
                            result["Revenue"] = data["claims"][key][0]["mainsnak"][
                                "datavalue"
                            ]["value"]["amount"]
                        elif key == "P8687":  # Social media followers
                            result["SocialMediaFollowers"] = data["claims"][key][0][
                                "mainsnak"
                            ]["datavalue"]["value"]["amount"]
                        elif key == "P2002":  # Twitter username
                            result["TwitterUser"] = data["claims"][key][0]["mainsnak"][
                                "datavalue"
                            ]["value"]

                        # humans
                    #     elif key == "P21":  # sex
                    #         if data["claims"][key][0]["mainsnak"]["datavalue"]["value"][
                    #             "id"
                    #         ] in ("Q6581097", "Q44148"):
                    #             result["sex"] = "male"
                    #         elif data["claims"][key][0]["mainsnak"]["datavalue"][
                    #             "value"
                    #         ]["id"] in ("Q6581072", "Q43445"):
                    #             result["sex"] = "female"
                    #         else:
                    #             result["sex"] = "other"
                    #     elif key == "P27":  # country of citizenship
                    #         result["country"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P106":  # occupation
                    #         result["occupation"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P22":  # father
                    #         result["father"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P25":  # mother
                    #         result["mother"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P40":  # children
                    #         result["number_of_children"] = len(data["claims"][key])
                    #     elif key == "P3373":  # siblings
                    #         result["number_of_siblings"] = len(data["claims"][key])
                    #     elif key == "P569":  # date of birth
                    #         result["date_of_birth"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["time"]
                    #     elif key == "P19":  # place of birth
                    #         result["place_of_birth"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["id"]
                    #     elif key == "P570":  # date of death
                    #         result["date_of_death"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["time"]
                    #     elif key == "P20":  # place of death
                    #         result["place_of_death"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["id"]
                    #     elif key == "P509":  # cause of death
                    #         result["cause_of_death"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["id"]
                    #     # locations
                    #     elif key == "P30":  # continent
                    #         result["continent"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P17":  # country
                    #         result["country"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P36":  # capital
                    #         result["capital"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P625":  # coordinate location
                    #         result["coordinates"] = (
                    #             str(
                    #                 data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                     "value"
                    #                 ]["latitude"]
                    #             )
                    #             + " "
                    #             + str(
                    #                 data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                     "value"
                    #                 ]["longitude"]
                    #             )
                    #         )
                    #     elif key == "P1082":  # population
                    #         result["population"] = float(
                    #             data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["amount"][1:]
                    #         )
                    #     elif key == "P2046":  # area
                    #         if (
                    #             "Q712226"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):  # km2
                    #             result["area"] = (
                    #                 data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                     "value"
                    #                 ]["amount"][1:]
                    #                 + " km2"
                    #             )
                    #     elif key == "P2049":  # width
                    #         result["width"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["amount"][1:]
                    #         if (
                    #             "Q828224"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["width"] += " km"
                    #         elif (
                    #             "Q11573"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["width"] += " m"
                    #     elif key == "P2043":  # length
                    #         result["length"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["amount"][1:]
                    #         if (
                    #             "Q828224"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["length"] += " km"
                    #         elif (
                    #             "Q11573"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["length"] += " m"
                    #     elif key == "P2044":  # elevation above sea level
                    #         result["height"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["amount"][1:]
                    #         if (
                    #             "Q828224"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["height"] += " km"
                    #         elif (
                    #             "Q11573"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["height"] += " m"
                    #     elif key == "P4511":  # vertical depth
                    #         result["height"] = (
                    #             "-"
                    #             + data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["amount"][1:]
                    #         )
                    #         if (
                    #             "Q828224"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["height"] += " km"
                    #         elif (
                    #             "Q11573"
                    #             in data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["unit"]
                    #         ):
                    #             result["height"] += " m"
                    #     # animals
                    #     elif key == "P4733":  # produced sound
                    #         result["sound"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P225":  # taxon name
                    #         result["latin"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]
                    #     # other
                    #     elif key == "P487":  # unicode character
                    #         result["emoji"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]
                    #     elif key == "P837":  # day in year for periodic occurance
                    #         result["date"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P571":  # inception
                    #         result["start_date"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["time"]
                    #         result["discovery_date"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["time"]
                    #     elif key == "P580":  # start time
                    #         result["start_date"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["time"]
                    #     elif key == "P582":  # end time
                    #         result["end_date"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["time"]
                    #     elif key == "P576":  # dissolved, abolished or demolished
                    #         result["end_date"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["time"]
                    #     elif key == "P169":  # chef executive officer
                    #         result["leader"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P6":  # head of government
                    #         result["leader"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P1120":  # number of deaths
                    #         result["deaths"] = float(
                    #             data["claims"][key][0]["mainsnak"]["datavalue"][
                    #                 "value"
                    #             ]["amount"][1:]
                    #         )
                    #     elif key == "P57":  # director
                    #         result["director"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P50":  # author
                    #         result["author"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P61":  # discoverer or inventor
                    #         result["discoverer"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P170":  # creator
                    #         result["discoverer"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P138":  # named after
                    #         result["discoverer"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P575":  # time of discovery or invention
                    #         result["discovery_date"] = data["claims"][key][0][
                    #             "mainsnak"
                    #         ]["datavalue"]["value"]["time"]
                    #     elif key == "P37":  # offical language
                    #         result["language"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P38":  # currency
                    #         result["currency"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]["id"]
                    #     elif key == "P246":  # element symbol
                    #         result["formula"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]
                    #     elif key == "P274":  # chemical formula
                    #         result["formula"] = data["claims"][key][0]["mainsnak"][
                    #             "datavalue"
                    #         ]["value"]

                    except KeyError:
                        pass
        return result
