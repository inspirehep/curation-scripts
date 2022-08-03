from inspirehep.curation.search_check_do import SearchCheckDo

OLD_PREFIX = "http://www.jetpletters.ac.ru"
NEW_PREFIX = "http://jetpletters.ru"

class MoveJETPLettersURLs(SearchCheckDo):
    """Move URLs pointing to JETP Letters to new domain."""

    query = f"urls.value:{OLD_PREFIX}*"

    @staticmethod
    def check(record, logger, state):
        return any(
            value.startswith(OLD_PREFIX)
            for value in record.get_value("urls.value", [])
        )

    @staticmethod
    def do(record, logger, state):
        urls = record.get("urls", [])
        for url in urls:
            if url["value"].startswith(OLD_PREFIX):
                url["value"] = url["value"].replace(
                    OLD_PREFIX, NEW_PREFIX
                )


MoveJETPLettersURLs()
