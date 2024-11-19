import json

import requests
from django.conf import settings


class DistributorApi:
    def __init__(self):
        self.base_url = "http://distributor.rules.api.pro.logitravel.internal"
        self.headers = {
            "Accept": "text/plain",
            "Authorization": settings.DISTRIBUTOR["PASSWORD"],
            "Content-Type": "application/json",
        }

    def get_level_closes(self):
        endpoint = "/api/organizations/lgt/agencies/products/hot/level_closes/"

        try:
            response = requests.get(
                f"{self.base_url}{endpoint}", headers=self.headers
            )
            response.raise_for_status()

            print("Rules retrieved successfully.")

            return response.json().get("rules", [])

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)

    def flatten_level_closes(self, rules):
        rules = json.loads(
            json.dumps(rules),
            object_hook=lambda obj: {**obj.pop("lvl", {}), **obj},
        )
        metadata = {
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
            "level_mapping": {
                "t": "level",
                "l": "list",
                "f": "from",
                "u": "to",
            },
        }

        for rule in rules:
            # Set default "rrg" if missing
            rrg = rule.get("rrg")
            if rrg is None:
                rule["rrg"] = {"f": 0, "t": 0, "u": 0}

            # Rename keys according to metadata
            for key in list(rule.keys()):
                if key in metadata:
                    rule[metadata[key]] = rule.pop(key)

            # Handle nested dictionary for level mapping
            level_mapping = metadata["level_mapping"]
            for key, value in rule.items():
                if isinstance(value, dict):
                    for k in list(value.keys()):
                        if k in level_mapping:
                            value[level_mapping[k]] = value.pop(k)

        return rules

    def create_level_closes(self, data):
        endpoint = (
            "/api/organizations/lgt/agencies/products/hot/level_closes/new"
        )

        if not data:
            print("No data received or data is empty.")

            return None

        try:
            response = requests.put(
                f"{self.base_url}{endpoint}", headers=self.headers, json=data
            )
            response.raise_for_status()

            print("Rule created successfully.")

            return response.json().get("rules", [])

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)

    def update_level_closes(self, rule_id, data):
        endpoint = f"/api/organizations/lgt/agencies/products/hot/level_closes/{rule_id}"

        if not data:
            print("No data received or data is empty.")

            return None

        try:
            response = requests.put(
                f"{self.base_url}{endpoint}", headers=self.headers, json=data
            )
            response.raise_for_status()

            print("Rule updated successfully.")

            return response.json().get("rules", [])

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Oops: Something Else", err)