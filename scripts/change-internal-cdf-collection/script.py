from inspirehep.curation.search_check_do import SearchCheckDo


class ChangeInternalCDFCollection(SearchCheckDo):
    """Ensure all CDF Internal Notes are really private."""

    query = '_collections:"CDF Internal Notes"'

    @staticmethod
    def check(record, logger, state):
        return len(record["_collections"]) > 1 and "CDF Internal Notes" in record["_collections"]

    @staticmethod
    def do(record, logger, state):
        record["_collections"] = ["CDF Internal Notes"]


ChangeInternalCDFCollection()
