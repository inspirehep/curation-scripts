from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class ReplaceEurophLetterWithEPL(SearchCheckDo):
    """Replace Europhys.Lett. in pubinfo with EPL"""

    query = "j Europhys.Lett. and not j EPL"

    @staticmethod
    def check(record, logger, state):
        return any(
            journal.lower() == "europhys.lett."
            for journal in get_value(record, "publication_info.journal_title", [])
        )

    @staticmethod
    def do(record, logger, state):
        for pubinfo in record["publication_info"]:
            if pubinfo.get("journal_title") == "Europhys.Lett.":
                pubinfo["journal_title"] = "EPL"


ReplaceEurophLetterWithEPL()
