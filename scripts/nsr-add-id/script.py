import requests

from inspirehep.curation.search_check_do import SearchCheckDo

URL = (
    "https://cernbox.cern.ch/remote.php/dav/public-files/"
    "yq254v51yVIdaQf/nsr-dois.json"
)

ELEMENT = "external_system_identifiers"


def get_unambiguous_ids(url):
    """Get a mapping from doi to NSR record ID, ignoring duplicate DOIs."""
    seen = set()
    result = {}
    data = requests.get(url).json()
    for nsr_id, doi in data.items():
        doi = doi.lower()
        if doi in seen:
            result.pop(doi, None)
        seen.add(doi)
        result[doi] = nsr_id
    return result


NSR_IDS = get_unambiguous_ids(URL)


class AddNSRIds(SearchCheckDo):
    """Add NNDC NSR IDs to INSPIRE records."""

    query = f"doi * -{ELEMENT}.schema:NSR"

    @staticmethod
    def check(record, logger, state):
        if any(id_["schema"] == "NSR" for id_ in record.get(ELEMENT, [])):
            return False
        for doi in record.get_value("dois.value", []):
            if doi.lower() in NSR_IDS:
                state["nsr_id"] = NSR_IDS[doi.lower()]
                return True
        return False

    @staticmethod
    def do(record, logger, state):
        record.setdefault(ELEMENT, []).append(
            {
                "value": NSR_IDS[state["nsr_id"]],
                "schema": "NSR",
            }
        )


AddNSRIds()
