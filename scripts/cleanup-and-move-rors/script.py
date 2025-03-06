from inspirehep.curation.search_check_do import SearchCheckDo
from itertools import chain
import re


class CleanupAndMoveRORs(SearchCheckDo):
    """Cleanup RORs from raw_affiliations and move them to affiliations_identifiers"""

    query = "authors.raw_affiliations.value:'ror.org'"

    @staticmethod
    def check(record, logger, state):
        ror_pattern = re.compile(r"https:\/\/ror\.org\/0\w{6}\d{2}")
        affiliations = chain.from_iterable(
            record.get_value("authors.raw_affiliations.value") or []
        )
        return any(ror_pattern.search(val) for val in affiliations)

    @staticmethod
    def do(record, logger, state):
        ror_pattern = re.compile(r"https:\/\/ror\.org\/0\w{6}\d{2}")
        for author in record.get("authors", []):
            for affiliation in author.get("raw_affiliations", []):
                ror = ror_pattern.search(affiliation["value"])
                if ror:
                    author.setdefault("affiliations_identifiers", []).append(
                        {"schema": "ROR", "value": ror.group(0)}
                    )
                    affiliation["value"] = re.sub(ror_pattern, "", affiliation["value"])
            author["affiliations_identifiers"] = [
                dict(t)
                for t in {tuple(d.items()) for d in author["affiliations_identifiers"]}
            ]


CleanupAndMoveRORs()
