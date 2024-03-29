from inspirehep.curation.search_check_do import SearchCheckDo

CNUM = "C23-05-07"
AUTHOR_LIST = [
    "Assmann, Ralph",
    "McIntosh, Peter",
    "Fabris, Alessandro",
    "Bisoffi, Giovanni",
    "Andrian, Ivan",
    "Vinicola, Giulia",
]
AUTHOR_QUERY = " and ".join(f"a {author}" for author in AUTHOR_LIST)


class RemoveWrongIPAC2023Authors(SearchCheckDo):
    """Remove incorrect authors on IPAC2023 papers due to bad JACoW metadata."""

    query = f"publication_info.cnum:{CNUM} and {AUTHOR_QUERY}"

    @staticmethod
    def check(record, logger, state):
        return (
            CNUM in record.get_value("publication_info.cnum", [])
            and record.get_value("authors.full_name", []) == AUTHOR_LIST
        )

    @staticmethod
    def do(record, logger, state):
        del record["authors"]


RemoveWrongIPAC2023Authors()
