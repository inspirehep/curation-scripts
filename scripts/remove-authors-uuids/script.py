from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class RemoveAuthorsUuids(SearchCheckDo):
    """Remove UUIDS for all the authors that doesn't have record.$ref"""

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "authors",
                            "query": {
                                "bool": {
                                    "must_not": {
                                        "exists": {"field": "authors.record.$ref"}
                                    }
                                }
                            },
                        }
                    },
                    {"match": {"_collections": "Literature"}},
                ]
            }
        }
    }

    def search(self):
        self.logger.info("Searching records", query=self.query)
        query = (
            self.search_class()
            .from_dict(self.query)
            .params(_source={}, size=self.size, scroll="60m")
        )
        if shard_filter := self._current_shard_filter():
            query = query.filter("script", script=shard_filter)
        return query.scan()

    @staticmethod
    def check(record, logger, state):
        return len(get_value(record, "authors.record.$ref", [])) < len(
            get_value(record, "authors", [])
        )

    @staticmethod
    def do(record, logger, state):
        for author in record["authors"]:
            author_ref = get_value(author, "record.$ref")
            if not author_ref:
                del author["uuid"]


RemoveAuthorsUuids()
