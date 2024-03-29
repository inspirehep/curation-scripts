from inspirehep.curation.search_check_do import SearchCheckDo
from inspirehep.oai.utils import is_cds_set, is_cern_arxiv_set


class ForceCDSHarvest(SearchCheckDo):
    """Touch records harvested by CDS to force synchronization after fixing bug."""

    query = (
        "(_oai.sets:CERN:arXiv or _oai.sets:ForCDS) "
        "and du > 2021-06-26 and du < 2023-01-28 "
        "and arxiv_eprints.value:* and de >= 2021"
    )

    @staticmethod
    def check(record, logger, state):
        return (
            is_cds_set(record)
            or is_cern_arxiv_set(record)
            and "arxiv_eprints" in record
        )

    @staticmethod
    def do(record, logger, state):
        # don't need to do anything here, just update the `update` timestamp as
        # a side-effect
        ...


ForceCDSHarvest()
