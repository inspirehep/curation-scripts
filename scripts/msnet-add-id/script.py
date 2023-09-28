import requests

from inspirehep.curation.search_check_do import SearchCheckDo

URL = (
    "https://cernbox.cern.ch/remote.php/dav/public-files/"
    "DgV3O0I8D8haXMZ/msnet_add_id.json"
)
MSNET_IDS = requests.get(URL).json()

ELEMENT = "external_system_identifiers"


class AddMsnetIds(SearchCheckDo):
    """Add MSNET IDs to INSPIRE records."""

    query = f"tc:p -{ELEMENT}.schema:MSNET"

    @staticmethod
    def check(record, logger, state):
        return record["control_number"] in MSNET_IDS and not any(
            id_["schema"] == "MSNET"
            for id_ in record.get("external_system_identifiers", [])
        )

    @staticmethod
    def do(record, logger, state):
        record.setdefault(ELEMENT, []).append(
            {
                "value": MSNET_IDS[record.get_value("control_number")],
                "schema": "MSNET",
            }
        )


AddMsnetIds()
