import json
from datetime import datetime

import pandas as pd
import requests

from config import Config


class DistributorApi:
    def __init__(self):
        self.base_url = "http://distributor.rules.api.pro.logitravel.internal"
        self.headers = {
            "Authorization": f"ApiKey {Config.APIKEY}",
            "Content-Type": "application/json",
        }

        self.metadata = {
            "editState": "edit_state",
            "isObsolete": "obsolete",
            "name": "name",
            "description": "description",
            "lastUser": "updated_by",
            "lastDate": "updated_on",
            "tag": "tag",
            "id": "id",
            "rrg": "range",
            "cli": "credential",
            "ps": "paying_society",
            "cp": "refundable",
            "rat": "rate",
            "prv": "provider",
            "hot": "hotel",
            "dest": "destination",
            "mrk": "market",
            "mel": "meal",
            "cid": "check_in",
            "bod": "booking_date",
            "rel": "max_release",
            "isDynamicCommission": "dynamic_commission",
            "dow": "days_of_week",
            "age": "age",
            "room": "room",
            "non": "num_of_nights",
            "hou": "hours",
            "level_mapping": {"t": "level", "l": "list", "f": "from", "u": "to"},
        }

    def get_stopsale_rules(self):
        endpoint = f"/api/organizations/lgt/agencies/products/hot/level_closes/"

        try:
            r = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
            r.raise_for_status()

            print("Rules retrieved successfully.")

            return r.json()

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)

    def stopsale_rules_to_df(self, data):
        # Flatten the "lvl" field into the main object
        data = json.loads(
            json.dumps(data), object_hook=lambda obj: {**obj.pop("lvl", {}), **obj}
        )
        rules = data.get("rules", [])

        for rule in rules:
            # Set default "rrg" if missing
            rrg = rule.get("rrg")
            if rrg is None:
                rule["rrg"] = {"f": 0, "t": 0, "u": 0}

            # Rename keys according to metadata
            for key in list(rule.keys()):
                if key in self.metadata:
                    rule[self.metadata[key]] = rule.pop(key)

            # Handle nested dictionary for level mapping
            level_mapping = self.metadata["level_mapping"]
            for key, value in rule.items():
                if isinstance(value, dict):
                    for k in list(value.keys()):
                        if k in level_mapping:
                            value[level_mapping[k]] = value.pop(k)

        return pd.json_normalize(rules, sep="_")

    def delete_rules(self, rule_ids, org):
        endpoint = f"/api/organizations/{org}/agencies/products/hot/level_closes/"
        print(endpoint)
        if rule_ids:
            try:
                r = requests.delete(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    data=json.dumps(rule_ids),
                )
                r.raise_for_status()

                print("Rules deleted successfully.")

                return r.json()

            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Oops: Something Else", err)
        else:
            print("No rule IDs provided.")
            return None

    def get_agencies(self):
        endpoint = "/api/organizations/lgt/agencies/"

        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print("Error: Agencies not found.")
                return None
            else:
                print(f"Error: Received unexpected status code {response.status_code}.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None