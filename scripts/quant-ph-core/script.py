from inspirehep.curation.search_check_do import SearchCheckDo
from inspirehep.utils import flatten_list


class SetQuantPhCore(SearchCheckDo):
    """Set all papers with quant-ph arXiv category as core."""

    query = "arxiv_eprints.categories:quant-ph"

    @staticmethod
    def check(record, logger, state):
        categories = flatten_list(record.get_value("arxiv_eprints.categories", []))
        return any(c == "quant-ph" for c in categories) and not record.get("core")

    @staticmethod
    def do(record, logger, state):
        record["core"] = True


SetQuantPhCore()
