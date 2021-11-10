from inspirehep.curation.search_check_do import SearchCheckDo


class MoveJETPURLs(SearchCheckDo):
    """Move URLs pointing to JETP to new domain."""

    query = 'urls.value:http://www.jetp.ac.ru*'

    @staticmethod
    def check(record, logger, state):
        return any(
            value.startswith("http://www.jetp.ac.ru")
            for value in record.get_value("urls.value", [])
        )

    @staticmethod
    def do(record, logger, state):
        urls = record.get("urls", [])
        for url in urls:
            if url["value"].startswith("http://www.jetp.ac.ru"):
                url["value"] = url["value"].replace(
                    "http://www.jetp.ac.ru", "http://www.jetp.ras.ru"
                )


MoveJETPURLs()
