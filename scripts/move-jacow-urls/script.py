from inspirehep.curation.search_check_do import SearchCheckDo

OLD_PREFIX = "http://accelconf.web.cern.ch/accelconf/"
NEW_PREFIX = "http://accelconf.web.cern.ch/"


class MoveJACOWURLs(SearchCheckDo):
    """Move URLs pointing to JETP to new domain."""

    query = "urls.value:http://accelconf.web.cern.ch/*"

    @staticmethod
    def check(record, logger, state):
        return any(
            value.lower().startswith(OLD_PREFIX)
            for value in record.get_value("urls.value", [])
        )

    @staticmethod
    def do(record, logger, state):
        urls = record.get("urls", [])
        for url in urls:
            if url["value"].lower().startswith(OLD_PREFIX):
                url["value"] = NEW_PREFIX + url["value"][len(OLD_PREFIX) :]


MoveJACOWURLs()
