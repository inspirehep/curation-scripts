import requests

from inspirehep.curation.search_check_do import SearchCheckDo

URL = (
    "https://cernbox.cern.ch/remote.php/dav/public-files/"
    "yq254v51yVIdaQf/nsr-dois.json"
)

ELEMENT = "external_system_identifiers"


def get_unambiguous_ids(url):
    """Get a mapping from doi to NSR record ID, ignoring duplicate ambiguous DOIs."""
    seen = set()
    result = {}
    data = requests.get(url).json()
    for nsr_id, doi in data:
        if doi in seen:
            result.pop(doi, None)
        seen.add(doi.lower())
        result[doi] = nsr_id
    return result


NSR_IDS = get_unambiguous_ids(URL)


class AddNSRIds(SearchCheckDo):
    """Add NNDC NSR IDs to INSPIRE records."""

    query = f"doi * -{ELEMENT}.schema:NSR"

    @staticmethod
    def check(record, logger, state):
        dois = record.set_value("dois.value", [])
        return str(record["control_number"]) in NSR_IDS and not any(
            id_["schema"] == "NSR"
            for id_ in record.get("external_system_identifiers", [])
        )

    @staticmethod
    def do(record, logger, state):
        record.setdefault(ELEMENT, []).append(
            {
                "value": NSR_IDS[str(record["control_number"])],
                "schema": "NSR",
            }
        )


AddMsnetIds()
