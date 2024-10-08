from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class RemoveClassifierKeywords(SearchCheckDo):
    query = "keywords.source:classifier"

    @staticmethod
    def check(record, logger, state):
        if any(
            keyword.get("source", "") == "classifier"
            for keyword in get_value(record, "keywords", [])
        ):
            return True
        else:
            return False

    @staticmethod
    def do(record, logger, state):
        new_keywords = [
            keyword
            for keyword in record.get("keywords", [])
            if keyword.get("source", "") != "classifier"
        ]
        if new_keywords:
            record["keywords"] = new_keywords
        else:
            del record["keywords"]


RemoveClassifierKeywords()
