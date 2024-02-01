from .loggers import console
import json

def issues_parser(issues: list):
    logs = []


    for issue in issues:
        logs.append(
            "ID: " + str(issue.get("id")) + 
            "SEVERIRY: " + str(issue.get("severity")) +
            "TITLE: " + str(issue.get("title")) +
            "DESCRIPTION: " + (str(issue.get("description")).replace('\n', " ")) +
            "REMEDIATION: " + (str(issue.get("remediation")).replace('\n', " ")) +
            "SNOOZED: " + str(issue.get("snoozed")) +
            "SNOOZE_REASON: " + str(issue.get("snooze_reason")) +
            "SNOOZE_UNTIL: " + str(issue.get("snooze_until")) +
            "OCCURRENCES: " + str(issue.get("occurrences"))
        )
    
    return logs

def occurrences_parser(occurrences):
    logs = []

    for occurrence in occurrences:
        logs.append(
            "ID: " + str(occurrence.get("id")) +
            "TARGET: " + str(occurrence.get("target")) +
            "PORT: " + str(occurrence.get("port")) +
            "EXTRA_INFO: " + str(occurrence.get("extra_info")) +
            "AGE: " + str(occurrence.get("age")) +
            "SNOOZED: " + str(occurrence.get("snoozed")) +
            "SNOOZE_REASON: " + str(occurrence.get("snooze_reason")) +
            "SNOOZE_UNTIL: " + str(occurrence.get("snooze_until"))
        )
    
    return logs

def scanner_output_parser(scanner_output):
    try:
        logs = []

        for output in scanner_output:
            log = ""
            for key, value in output[0].items():
                if key == "plugin":
                    log += "CVE: " + str(value.get("cve"))
                    log += "CVSS_BASE_SCORE: " + str(value.get("cvss_base_score"))
                    log += "CVSS3_BASE_SCORE: " + str(value.get("cvss3_base_score"))
                    log += "NAME: " + str(value.get("name"))
                elif key == "scanner_output":
                    log += "SCANNER_OUTPUT: " + str(value).replace('\n', " ")
                else:
                    log += str(key).upper() + ": " + str(value)
            
            logs.append(log)
        
        return logs
    except Exception as e:
        console.error("Error in scanner_output_parser: " + str(e))
        return []
