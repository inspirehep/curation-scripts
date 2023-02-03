from itertools import chain
from inspire_utils.record import get_value, get_values_for_schema
from inspirehep.curation.search_check_do import SearchCheckDo


class RemoveAuthorsBai(SearchCheckDo):
    """Remove BAI from literature records"""

    query = 'authors.ids.schema:"INSPIRE BAI"'

    @staticmethod
    def check(record, logger, state):
        authors_ids = get_value(record, "authors.ids", [])
        return next(
            chain.from_iterable(
                get_values_for_schema(author_ids, "INSPIRE BAI")
                for author_ids in authors_ids
            ),
            False,
        )

    @staticmethod
    def do(record, logger, state):
        for author in record["authors"]:
            author_ids = author.get('ids')
            if not author_ids:
                continue
            new_ids = [
                id_dict for id_dict in author_ids if id_dict["schema"] != "INSPIRE BAI"
            ]
            if new_ids:
                author["ids"] = new_ids
            else:
                del author["ids"]


RemoveAuthorsBai()
