from inspirehep.curation.search_check_do import SearchCheckDo

FULLTEXT_URL = "https://jacow.org/rupac2021/papers/{}.pdf"


class FixRupac2021Fulltexts(SearchCheckDo):
    """Fix fulltexts for RuPAC 2021 (Alushta, Crimea)."""

    query = "publication_info.conference_record.$ref:1954430"

    @staticmethod
    def check(record, logger, state):
        return "C21-09-27.4" in record.get_value("publication_info.cnum", [])

    @staticmethod
    def do(record, logger, state):
        artids = record.get_value("publication_info.artid", [])
        if len(artids) != 1:
            logger.warning("Ambiguous article IDs.", artids=artids)
            return
        if (num_docs := len(record.get("documents", []))) != 1:
            logger.warning("Ambiguous or missing documents.", num_docs=num_docs)
            return
        artid = artids[0].lower()
        record["documents"] = [{"url": FULLTEXT_URL.format(artid)}]


FixRupac2021Fulltexts()
