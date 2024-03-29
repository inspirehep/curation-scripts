from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class ReplaceEurophLetterWithEPLInRefs(SearchCheckDo):
    """Replace Europhys.Lett. in pubinfo with EPL"""

    query = "references.reference.publication_info.journal_title:europhys.lett."

    @staticmethod
    def check(record, logger, state):
        return any(
            ref_journal.lower() == "europhys.lett."
            for ref_journal in get_value(
                record, "references.reference.publication_info.journal_title", []
            )
        )

    @staticmethod
    def do(record, logger, state):
        for reference in record["references"]:
            ref_journal_title = get_value(
                reference, "reference.publication_info.journal_title", ""
            )
            if ref_journal_title.lower() == "europhys.lett.":
                reference["reference"]["publication_info"]["journal_title"] = "EPL"


ReplaceEurophLetterWithEPLInRefs()
