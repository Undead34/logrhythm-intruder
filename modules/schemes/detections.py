import jsonschema

detections_schema = {
    "type": "object",
    "properties": {
        "source": {"type": "string"},
        "uuid": {"type": "string"},
        "detectedDateTime": {"type": "string"},
        "ingestedDateTime": {"type": "string"},
        "entityType": {"type": "string"},
        "entityName": {"type": "string"},
        "filters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "highlightedObjects": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "field": {"type": "string"},
                                "type": {"type": "string"},
                                "value": {"type": "string"},
                            },
                        },
                    },
                    "mitreTacticIds": {"type": "array", "items": {"type": "string"}},
                    "mitreTechniqueIds": {"type": "array", "items": {"type": "string"}},
                    "riskLevel": {"type": "string"},
                    "type": {"type": "string"},
                },
            },
        },
        "detail": {
            "type": "object",
            "properties": {
                "uuid": {"type": "string"},
                "filterRiskLevel": {"type": "string"},
                "endpointHostName": {"type": "string"},
                "endpointGUID": {"type": "string"},
                "objectFilePath": {"type": "string"},
                "objectFileHashSha1": {"type": "string"},
                "objectFileHashSha256": {"type": "string"},
                "objectFileHashMd5": {"type": "string"},
                "processCmd": {"type": "string"},
                "objectType": {"type": "string"},
                "processFilePath": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "tacticId": {"type": "array", "items": {"type": "string"}},
                "ruleName": {"type": "string"},
                "eventName": {"type": "string"},
                "eventSubName": {"type": "string"},
                "parentCmd": {"type": "string"},
                "parentFilePath": {"type": "string"},
                "parentFileHashSha1": {"type": "string"},
                "parentFileHashSha256": {"type": "string"},
                "parentFileHashMd5": {"type": "string"},
                "processFileHashSha1": {"type": "string"},
                "processFileHashSha256": {"type": "string"},
                "processFileHashMd5": {"type": "string"},
                "eventId": {"type": "string"},
                "policyId": {"type": "string"},
                "productCode": {"type": "string"},
                "pname": {"type": "string"},
                "act": {"type": "array", "items": {"type": "string"}},
                "deviceGUID": {"type": "string"},
                "instanceId": {"type": "string"},
                "processName": {"type": "string"},
                "processPid": {"type": "integer"},
                "parentPid": {"type": "integer"},
                "eventTime": {"type": "string"},
                "eventSourceType": {"type": "integer"},
                "rt_utc": {"type": "string"},
                "rt": {"type": "string"},
                "behaviorCat": {"type": "string"},
                "engineOperation": {"type": "string"},
                "engVer": {"type": "string"},
                "mpname": {"type": "string"},
                "mpver": {"type": "string"},
                "patVer": {"type": "string"},
                "processSigner": {"type": "array", "items": {"type": "string"}},
                "riskLevel": {"type": "string"},
                "parentName": {"type": "string"},
                "parentSigner": {"type": "array", "items": {"type": "string"}},
                "parentSignerValid": {"type": "array", "items": {"type": "boolean"}},
                "processSignerValid": {"type": "array", "items": {"type": "boolean"}},
                "logKey": {"type": "string"},
                "processHashId": {"type": "string"},
                "parentHashId": {"type": "string"},
                "objectFileSize": {"type": "string"},
            },
        },
        "endpoint": {
            "type": "object",
            "properties": {
                "ips": {"type": "array", "items": {"type": "string"}},
                "agentGuid": {"type": "string"},
                "endpointName": {"type": "string"},
            },
        },
    },
}

class DetectionsSchema:
    def __init__(self) -> None:
        self.validator = jsonschema.Draft7Validator(detections_schema)
        self.validator.check_schema(detections_schema)

    def isValid(self, data: dict) -> bool:
        try:
            self.validator.validate(data)
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False
        except Exception as e:
            print(e)
            return False

    # object is a valid detection_schema
    # This function returns a string un KEY: VALUE format with all relevant information of detection_shema considering the security in the mind
    def parser(self, object: dict):
        try:
            detections = ""
            detections += "Source: " + object.get("source")
            detections += "UUID: " + object.get("uuid")
            detections += "Detected Date Time: " + object.get("detectedDateTime")
            detections += "Ingested Date Time: " + object.get("ingestedDateTime")
            detections += "Entity Type: " + object.get("entityType")
            detections += "Entity Name: " + object.get("entityName")

            object_details: dict = object.get("detail")

            details = ""
            details += "Details UUID: " + str(object_details.get("uuid"))
            details += "Filter Risk Level: " + str(object_details.get("filterRiskLevel"))
            details += "Endpoint Host Name: " + str(object_details.get("endpointHostName"))
            details += "Endpoint GUID: " + str(object_details.get("endpointGUID"))
            details += "Object File Path: " + str(object_details.get("objectFilePath"))
            details += "Object File Hash Sha1: " + str(object_details.get("objectFileHashSha1"))
            details += "Object File Hash Sha256: " + str(object_details.get("objectFileHashSha256"))
            details += "Object File Hash Md5: " + str(object_details.get("objectFileHashMd5"))
            details += "Process Cmd: " + str(object_details.get("processCmd"))
            details += "Object Type: " + str(object_details.get("objectType"))
            details += "Process File Path: " + str(object_details.get("processFilePath"))
            details += "Tags: " + str(object_details.get("tags"))
            details += "Tactic Id: " + str(object_details.get("tacticId"))
            details += "Rule Name: " + str(object_details.get("ruleName"))
            details += "Event Name: " + str(object_details.get("eventName"))
            details += "Event Sub Name: " + str(object_details.get("eventSubName"))
            details += "Parent Cmd: " + str(object_details.get("parentCmd"))
            details += "Parent File Path: " + str(object_details.get("parentFilePath"))
            details += "Parent File Hash Sha1: " + str(object_details.get("parentFileHashSha1"))
            details += "Parent File Hash Sha256: " + str(object_details.get("parentFileHashSha256"))
            details += "Parent File Hash Md5: " + str(object_details.get("parentFileHashMd5"))
            details += "Process File Hash Sha1: " + str(object_details.get("processFileHashSha1"))
            details += "Process File Hash Sha256: " + str(object_details.get("processFileHashSha256"))
            details += "Process File Hash Md5: " + str(object_details.get("processFileHashMd5"))
            details += "Event Id: " + str(object_details.get("eventId"))
            details += "Policy Id: " + str(object_details.get("policyId"))
            details += "Product Code: " + str(object_details.get("productCode"))
            details += "Pname: " + str(object_details.get("pname"))
            details += "Act: " + str(object_details.get("act"))
            details += "Device GUID: " + str(object_details.get("deviceGUID"))
            details += "Instance Id: " + str(object_details.get("instanceId"))
            details += "Process Name: " + str(object_details.get("processName"))
            details += "Process Pid: " + str(object_details.get("processPid"))
            details += "Parent Pid: " + str(object_details.get("parentPid"))
            details += "Event Time: " + str(object_details.get("eventTime"))
            details += "Event Source Type: " + str(object_details.get("eventSourceType"))
            details += "Rt Utc: " + str(object_details.get("rt_utc"))
            details += "Rt: " + str(object_details.get("rt"))
            details += "Behavior Cat: " + str(object_details.get("behaviorCat"))
            details += "Engine Operation: " + str(object_details.get("engineOperation"))
            details += "Eng Ver: " + str(object_details.get("engVer"))
            details += "Mpname: " + str(object_details.get("mpname"))
            details += "Mpver: " + str(object_details.get("mpver"))
            details += "Pat Ver: " + str(object_details.get("patVer"))
            details += "Process Signer: " + str(object_details.get("processSigner"))
            details += "Risk Level: " + str(object_details.get("riskLevel"))
            details += "Parent Name: " + str(object_details.get("parentName"))
            details += "Parent Signer: " + str(object_details.get("parentSigner"))
            details += "Parent Signer Valid: " + str(object_details.get("parentSignerValid"))
            details += "Process Signer Valid: " + str(object_details.get("processSignerValid"))
            details += "Log Key: " + str(object_details.get("logKey"))
            details += "Process Hash Id: " + str(object_details.get("processHashId"))
            details += "Parent Hash Id: " + str(object_details.get("parentHashId"))
            details += "Object File Size: " + str(object_details.get("objectFileSize"))

            detections += details

            endpoint = object.get("endpoint")
            endpoints = ""
            endpoints += "IPS: " + str(endpoint.get("ips"))
            endpoints += "Agent GUID: " + str(endpoint.get("agentGuid"))
            endpoints += "Endpoint Name: " + str(endpoint.get("endpointName"))
            detections += endpoints

            filters = object.get("filters")
            filter = ""
            
            for x in range(len(filters)):
                filter += "ID: " + str(filters[x].get("id"))
                filter += "Name: " + str(filters[x].get("name"))
                filter += "Description: " + str(filters[x].get("description"))
                highlightedObjects = filters[x].get("highlightedObjects")
                highlightedObject = ""
                for y in range(len(highlightedObjects)):
                    highlightedObject += "Field: " + str(highlightedObjects[y].get("field"))
                    highlightedObject += "Type: " + str(highlightedObjects[y].get("type"))
                    highlightedObject += "Value: " + str(highlightedObjects[y].get("value"))
                filter += "Highlighted Objects: " + highlightedObject
                filter += "Mitre Tactic Ids: " + str(filters[x].get("mitreTacticIds"))
                filter += "Mitre Technique Ids: " + str(filters[x].get("mitreTechniqueIds"))
                filter += "Risk Level: " + str(filters[x].get("riskLevel"))
                filter += "Type: " + str(filters[x].get("type"))
                detections += filter

            return detections
        except Exception as e:
            print(e)
            return str(object)