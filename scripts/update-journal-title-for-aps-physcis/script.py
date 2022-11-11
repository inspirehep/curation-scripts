from inspire_utils.record import get_value
from inspirehep.curation.search_check_do import SearchCheckDo


class UpdateJournalTitleForApsPhysics(SearchCheckDo):
    """
    Update journal title for journals with source=`APS`
    and title `Physcis` to `APS Physics`
    """

    query = {
        "_source": "control_number",
        "query": {
            "bool": {
                "must": [
                    {"match": {"journal_title_variants": "Physics"}},
                    {"match": {"acquisition_source.source": "APS"}},
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
        journal_titles = [
            pubinfo.get("journal_title")
            for pubinfo in record.get("publication_info", [])
        ]
        return (
            "Physics" in journal_titles
            and get_value(record, "acquisition_source.source") == "APS"
        )

    @staticmethod
    def do(record, logger, state):
        for publication_info in record["publication_info"]:
            if publication_info.get("journal_title") == "Physics":
                publication_info["journal_title"] = "APS Physics"


UpdateJournalTitleForApsPhysics()
