from .loggers import console
import binascii

def parseOATEvents(output):
    console.debug("Preparing to parse OAT detections...")
    totalCount = output.get("totalCount")
    count = output.get("count")
    items = output.get("items")
    OATs = []

    if count < totalCount:
        console.warn(
            f"There are more detections than the ones shown. Please, increase the 'top' parameter. (Current: {count}, Total: {totalCount})"
        )

    for i in range(len(items)):
        item = items[i]
        if item.get("source") == "detections":
            data = convert_object(item)
            selected_keys = {
                "SOURCE",
                "UUID",
                "DETECTEDDATETIME",
                "INGESTEDDATETIME",
                "ENTITYTYPE",
                "ENTITYNAME",
                "ENDPOINTNAME",
                "IPS",
                "FILTERRISKLEVEL",
                "ENDPOINTHOSTNAME",
                "PROCESSCMD",
                "OBJECTTYPE",
                "PROCESSFILEPATH",
                "TAGS",
                "TACTICID",
                "RULENAME",
                "EVENTNAME",
                "EVENTSUBNAME",
                "PARENTCMD",
                "PARENTFILEPATH",
                "PARENTFILEHASHSHA256",
                "PROCESSFILEHASHSHA256",
                "POLICYID",
                "PROCESSNAME",
                "PROCESSPID",
                "PARENTPID",
                "PROCESSFILEPATH",
                "PROCESSCMD",
            }

            selected_elements, other_elements = process_object(data, selected_keys)

            OATs.append("".join(selected_elements + other_elements).replace("\n", ""))
        else:
            data = convert_object(item)
            selected_keys = {
                "ENTITYNAME",
                "DESCRIPTION",
                "MITRETACTICIDS",
                "MITRETECHNIQUEIDS",
                "ENDPOINTNAME",
                "IPS",
                "ENDPOINTHOSTNAME",
                "OSDESCRIPTION",
                "PROCESSHASHID",
                "PROCESSNAME",
                "PROCESSPID",
                "PROCESSUSER",
                "PROCESSUSERDOMAIN",
                "PROCESSLAUNCHTIME",
                "PROCESSCMD",
                "PROCESSFILEHASHID",
                "PROCESSFILEPATH",
                "PROCESSFILEHASHSHA256",
                "OBJECTUSER",
                "OBJECTUSERDOMAIN",
                "OBJECTSESSIONID",
                "OBJECTFILEPATH",
                "OBJECTFILEHASHSHA256",
                "OBJECTFILESIZE",
                "OBJECTNAME",
                "OBJECTPID",
                "OBJECTCMD",
                "OBJECTRUNASLOCALACCOUNT",
                "TAGS",
            }
            selected_elements, other_elements = process_object(data, selected_keys)
            OATs.append("".join(selected_elements + other_elements).replace("\n", ""))
            

    print("Número de OATs: " + str(output["count"]))
    print("Número de OATs válidos: " + str(len(OATs)))
    print("Número de OATs inválidos: " + str(output["count"] - len(OATs)))
    return OATs

def process_object(data, selected_keys):
    selected_elements = []
    other_elements = []

    for item in data:
        for key, value in item.items():
            if (key == "OBJECTRAWDATASTR" or key == "HIGHLIGHTEDOBJECTS"):
                value: bytes = value.encode()
                if not value.isascii():
                    value = binascii.b2a_base64(value)
                else:
                    value = value.decode().replace("\n", "")

            if key in selected_keys:
                selected_elements.append(f"{key.upper()}: {value}")
            else:
                other_elements.append(f"{key.upper()}: {value}")

    # Ordena las listas alfabéticamente
    selected_elements.sort()
    other_elements.sort()

    return selected_elements, other_elements

def convert_object(data):
    converted_data = []

    # Ordena las claves alfabéticamente, excluyendo "filters"
    for key in sorted(data.keys()):
        if key != "filters":
            if isinstance(data[key], dict):
                # Recurre a objetos anidados (como "detail")
                converted_data.extend(convert_object(data[key]))
            else:
                if key == "msg":
                    if type(data[key]) == str:
                        data[key] = data[key].encode()
                    data[key] = binascii.b2a_base64(data[key])
                
                converted_data.append({f"{key.upper()}": str(data[key])})

    # Procesa los "filters" al final, ordenando sus claves también
    if "filters" in data:
        for filter_data in data["filters"]:
            for key in sorted(filter_data.keys()):
                converted_data.append(
                    {f"{key.upper()}": str(filter_data[key])}
                )  # Aquí estaba el error

    return converted_data
