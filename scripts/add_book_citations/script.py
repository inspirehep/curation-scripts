from itertools import chain
from inspirehep.curation.search_check_do import SearchCheckDo

BOOKS = [
    {
        "recid": "2735748",
        "book_info": [
            "Rezzolla",
            "Zanotti",
            "Relativistic Hydrodynamics",
            "Oxford University Press",
            "2013",
        ],
    },
    {
        "recid": "181166",
        "book_info": [
            "Birrell",
            "Davies",
            "Quantum Fields in Curved Space",
            "Cambridge University Press",
            "1982",
        ],
    },
    {
        "recid": "159194",
        "book_info": ["Itzykson", "Zuber", "Quantum Field Theory", "McGraw", "1980"],
    },
    {
        "recid": "640063",
        "book_info": ["Dodelson", "Modern Cosmology", "Academic Press", "2003"],
    },
    {
        "recid": "1120339",
        "book_info": [
            "Baxter",
            "Exactly solved models in statistical mechanics",
            "Academic Press",
            "1982",
        ],
    },
]


class AddBookCitations(queryCheckDo):
    """Add recid to reference for the citation of a book."""

    query = ""
    book = BOOKS[0]
    book_info = book["book_info"]
    recid = book["recid"]
    url = f"https://inspirehep.net/api/literature/{recid}"
    for element in book_info:
        query += f" ft:{element}"
    query = f"{query} -refersto:recid:{recid}"

    @staticmethod
    def check(record, logger, state):
        global url
        cited_records = chain.from_iterable(
            record.get_value("references.record.ref", [])
        )
        return url in cited_records

    @staticmethod
    def do(record, logger, state):
        global book_info
        try:
            references = record["references"]
        except KeyError:
            return None
        for reference in record["references"]:
            try:
                raw_ref = reference.get("raw_refs", {})[0]["value"].lower()
            except KeyError:
                continue
            if all(book_element.lower() in raw_ref for book_element in book_info):
                references["record"]["$ref"] = url


AddBookCitations()
