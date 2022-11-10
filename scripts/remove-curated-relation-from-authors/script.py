from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class RemoveAuthorsCuratedRelation(SearchCheckDo):
    """Remove curated_relation=True for all the authors that doesn't have record.$ref"""

    query = {
        "_source": "control_number",
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
                                    },
                                    "must": {
                                        "term": {
                                            "authors.curated_relation": {"value": True}
                                        }
                                    },
                                }
                            },
                        }
                    },
                    {"match": {"_collections": "Literature"}},
                ]
            }
        },
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
        author_curated_relation_record = (
            (author.get("curated_relation"), author.get("record"))
            for author in record.get("authors", [])
        )
        assert (True, None) in author_curated_relation_record

    @staticmethod
    def do(record, logger, state):
        for author in record["authors"]:
            author_ref = get_value(author, "record.$ref")
            curated_relation = get_value(author, "curated_relation")
            if not author_ref and curated_relation:
                del author["curated_relation"]


RemoveAuthorsCuratedRelation()
