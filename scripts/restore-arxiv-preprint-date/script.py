from datetime import datetime
from inspirehep.curation.search_check_do import SearchCheckDo


class RestoreArxivPreprintDate(SearchCheckDo):
    """Restore the correct preprint_date which got overwritten due to an arXiv OAI-PMH bug."""

    query = "da < 2025-06-16 and arxiv_eprints.value:* and preprint_date:2025-06-16->2025-07-01"

    @staticmethod
    def check(record, logger, state):
        return (
            record.created < datetime(2025, 6, 16, 8)
            and record.get("preprint_date", "0") >= "2025-06-16"
        )

    @staticmethod
    def do(record, logger, state):
        current_preprint_date = record["preprint_date"]
        for revision_id in range(2, record.revision_id + 2):
            preprint_date = record.revisions[-revision_id].get("preprint_date")
            if preprint_date and preprint_date != current_preprint_date:
                record["preprint_date"] = preprint_date
                return
        logger.warning("Preprint date not modified")


RestoreArxivPreprintDate()
