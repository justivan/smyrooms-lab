import json

import requests

from config import Config


class DistributorApi:
    def __init__(self):
        self.base_url = "http://distributor.rules.api.pro.logitravel.internal"
        self.headers = {
            "Accept": "text/plain",
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

    def get_all_rules(self):
        endpoint = f"/api/organizations/lgt/agencies/products/hot/level_closes/"
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)

        if response.status_code == 200:
            data = response.json()

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

            return rules
        return None

    def delete_rules(self, rule_ids):
        endpoint = "/api/organizations/lgt/agencies/products/hot/level_closes/"

        if rule_ids:
            try:
                response = requests.delete(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    data=json.dumps(rule_ids),
                )

                if response.status_code == 200:
                    print("Rules deleted successfully.")
                elif response.status_code == 404:
                    print("Error: Rules not found.")
                else:
                    print(
                        f"Error: Received unexpected status code {response.status_code}."
                    )

                return response

            except requests.exceptions.RequestException as e:
                # Handle network-related errors
                print(f"An error occurred: {e}")
                return None
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
