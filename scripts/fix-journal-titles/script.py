from inspirehep.curation.search_check_do import SearchCheckDo

WRONG_JOURNALS_MAPPING = {
  "p.r.x.quantum.": "PRX Quantum",
  
}

class FixJournalTitles(SearchCheckDo):
    """Fix incorrectly normalized journal titles."""

    # Literature is default, ``search_class`` needs to be set for other
    # collections
    # search_class = LiteratureSearch

    query = " or ".join(
        f'j "{wrong_title}" or references.reference.publication_info.journal_title:"{wrong_title}"'
        for wrong_title in WRONG_JOURNALS_MAPPING
    )

    @staticmethod
    def check(record, logger, state):
        for wrong_title in WRONG_JOURNALS_MAPPING:
            wrong_in_pubinfo = any(title.lower() == wrong_title for title in record.get_value("publication_info.journal_title"))
            if wrong_in_pubinfo:
                retrun True
            # similar for references

    @staticmethod
    def do(record, logger, state):
        for pub_info in record.get("publication_info", []):
            if wrong_title := pub_info.get("journal_title", "").lower() in WRONG_JOURNAL_MAPPING:
                pub_info["journal_title"] = WRONG_JOURNAL_MAPPING[wrong_title]
        # same for references


FixJournalTitles()
