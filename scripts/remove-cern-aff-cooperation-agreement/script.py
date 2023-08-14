from inspire_utils.record import get_value
from inspire_utils.dedupers import dedupe_list
from inspirehep.curation.search_check_do import SearchCheckDo

RAW_AFFS = {
    "Affiliated with an institute covered by a cooperation agreement with CERN",
    "Affiliated with an international laboratory covered by a cooperation"
    " agreement with CERN",
}


def has_cooperation_agreement_raw_aff(author):
    return RAW_AFFS & set(
        get_value({"author": author}, "author.raw_affiliations.value", [])
    )


class RemoveCERNAffiliationCooperationAgreement(SearchCheckDo):
    """Remove incorrect CERN aff for authors having only a cooperation agreement."""

    query = (
        'authors.raw_affiliations.value:"Affiliated with an institute covered by'
        ' a cooperation agreement with CERN"'
    )

    @staticmethod
    def check(record, logger, state):
        return any(
            "CERN" in get_value({"author": a}, "author.affiliations.value", [])
            and has_cooperation_agreement_raw_aff(a)
            for a in record.get("authors", [])
        )

    @staticmethod
    def do(record, logger, state):
        for author in record["authors"]:
            if not has_cooperation_agreement_raw_aff(author):
                continue
            new_affs = []
            for aff in author["affiliations"]:
                if aff["value"] == "CERN":
                    new_affs.append(
                        {
                            "value": "Unlisted",
                            "record": {
                                "$ref": "https://inspirehep.net/api/institutions/910325"
                            },
                        }
                    )
                else:
                    new_affs.append(aff)
            author["affiliations"] = dedupe_list(new_affs)


RemoveCERNAffiliationCooperationAgreement()
