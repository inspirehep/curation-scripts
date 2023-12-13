from itertools import permutations

from inspirehep.curation.search_check_do import SearchCheckDo


class FixAPSHarvestingMess(SearchCheckDo):
    """Fix metadata issues caused by harvesting APS when fulltext API was broken."""

    query = "doi 10.1103* and du 2023-11-28->2024-01-01"

    @staticmethod
    def check(record, logger, state):
        state["to_delete"] = []

        enumerated_pubinfo_pairs = permutations(
            enumerate(record.get("publication_info", [])), r=2
        )
        for (i, pubinfo1), (_, pubinfo2) in enumerated_pubinfo_pairs:
            if pubinfo1.items() <= pubinfo2.items():
                state["to_delete"].append(i)

        return bool(state["to_delete"])

    @staticmethod
    def do(record, logger, state):
        new_pubinfo = [
            p
            for (p, i) in enumerate(record["publication_info"])
            if i not in state["to_delete"]
        ]
        record["publication_info"] = new_pubinfo


FixAPSHarvestingMess()
