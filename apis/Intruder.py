import requests
import json

from .BaseAPI import BaseAPI
from modules.constants import config
from modules.parsers import issues_parser, occurrences_parser, scanner_output_parser
from modules.loggers import Logger, console
import string


class Intruder(BaseAPI):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        issues = self.get_issues_list()
        occurrences = self.get_issues_occurrences(issues)
        self.get_issues_occurrences_scanner_output(issues, occurrences)

    def get_issues_list(self):
        # Get issues list
        console.debug("Obteniendo lista de issues...")
        url_issues = "https://api.intruder.io/v1/issues/"
        issues = self.get_items(url_issues).get("results")

        logs = issues_parser(issues)

        for log in logs:
            for w in string.whitespace:
                log = log.replace(w, " ")
            self.logger.issues(log.strip())

        return issues

    def get_issues_occurrences(self, issues):
        console.debug("Obteniendo ocurrencias de los issues...")
        occurrences = []

        for issue in issues:
            try:
                url_occurrences = (
                    f"https://api.intruder.io/v1/issues/{issue['id']}/occurrences/"
                )
                t = self.get_items(url_occurrences).get("results")

                for occurrence in t:
                    occurrence["issue"] = issue["id"]
                    occurrences.append(occurrence)
            except Exception as e:
                console.error(e)
                continue

        logs = occurrences_parser(occurrences)

        for log in logs:
            for w in string.whitespace:
                log = log.replace(w, " ")
            self.logger.occurrences(log.strip())

        return occurrences

    def get_issues_occurrences_scanner_output(self, issues, occurrences):
        try:
            console.debug("Obteniendo scanner output de las ocurrencias...")

            ids_scanner_output = set()
            scanner_output = []

            for issue in issues:
                for occurrence in occurrences:
                    if issue["id"] == occurrence["issue"]:
                        ids_scanner_output.add(f"{occurrence['id']}, {issue['id']}")
            
            # 
            console.debug(f"Preparing to get {len(ids_scanner_output)}")
            progess = 0

            for id in ids_scanner_output:
                try:
                    occurrence_id, issue_id = id.split(", ")
                    url_scanner_output = f"https://api.intruder.io/v1/issues/{issue_id}/occurrences/{occurrence_id}/scanner_output/"
                    scanner_output.append(self.get_items(url_scanner_output).get("results"))

                    progess += 1
                    console.debug(f"Progress: {progess}/{len(ids_scanner_output)}")
                except Exception as e:
                    console.error(e)
                    continue
                
            
            logs = scanner_output_parser(scanner_output)

            for log in logs:
                for w in string.whitespace:
                    log = log.replace(w, " ")
                self.logger.scanner_output(log.strip())

        except Exception as e:
            print(e)


    def get_items(self, url_path, params=None, headers=None):
        items = []
        count = 0
        next_link = None
        results = {}

        while True:
            if next_link is None:
                r = self.fetch(url_path, params=params, headers=headers)
            else:
                r = self.fetch(next_link, params=params, headers=headers)

            items.extend(r.get("results"))

            if "count" in r:
                count += r["count"]

            if not r["next"]:
                results = r
                r["results"] = items
                break

            next_link = r["next"]

        return results

    def fetch(self, url_issues, params=None, headers=None):
        headers = {
            "accept": "application/json",
            "Authorization": config["api"]["token"],
        }

        r = requests.get(url_issues, headers=headers)
        
        if 200 == r.status_code:
            if "application/json" in r.headers.get("Content-Type", ""):
                return r.json()
            return r.content
        else:
            print(r.status_code, r.text, url_issues)

    @staticmethod
    def api_check_connection():
        headers = {
            "Authorization": f"Bearer {config['api']['token']}",
        }

        r = requests.get("https://api.intruder.io/v1/health", headers=headers)

        if r.status_code == 401:
            return 401, "El token de acceso es inválido."
        elif r.status_code != 200:
            return r.status_code, "No se ha podido establecer conexión con el endpoint."
        return 200, "Conexión con el endpoint establecida."
