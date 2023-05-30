import requests

from inspirehep.curation.search_check_do import SearchCheckDo

URL = 'https://cernbox.cern...msnet_add_id.txt'
MSNET_IDS = requests.get(URL)

ELEMENT = 'external_system_identifiers'

class AddMsnetIds(SearchCheckDo):
    """Add MSNET IDs to INSPIRE records."""

    query = f'tc:p -{ELEMENT}.schema:MSNET'

    @staticmethod
    def check(record, logger, state):
        if record.get_value('control_number') not in MSNET_IDS:
            return True
        for schema in record.get_value(f'{ELEMENT}.schema', []):
            if schema == 'MSNET':
                return True
        return False

    @staticmethod
    def do(record, logger, state):
        record.setdefault(ELEMENT, []).append(
            {
                "value": MSNET_IDS[record.get_value('control_number')],
                "schema": "MSNET",
            }
        )


AddMsnetIds()
