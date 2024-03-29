from inspirehep.search.api import JobsSearch
from inspirehep.curation.search_check_do import SearchCheckDo


class FixLegacyJobsDeadlines(SearchCheckDo):
    """Fix legacy jobs with fake 'deadline_date=3000'"""

    search_class = JobsSearch
    query = "deadline_date:3000"

    @staticmethod
    def check(record, logger, state):
        has_deadline_3000 = record.get("deadline_date") == "3000"
        if has_deadline_3000:
            return True
        return False

    @staticmethod
    def do(record, logger, state):
        legacy_version = record.get("legacy_version")
        if legacy_version:
            year, month, day = (
                legacy_version[:4],
                legacy_version[4:6],
                legacy_version[6:8],
            )
            date = f"{year}-{month}-{day}"
            record["deadline_date"] = date
            record.setdefault("_private_notes", []).append(
                {
                    "value": "Record with no deadline,"
                    " fake 'deadline_date' derived from 'legacy_version'"
                }
            )
        else:
            record["deadline_date"] = record["legacy_creation_date"]
            record.setdefault("_private_notes", []).append(
                {
                    "value": "Record with no deadline,"
                    " fake 'deadline_date' derived from 'legacy_creation_date'"
                }
            )


FixLegacyJobsDeadlines()
