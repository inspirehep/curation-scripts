from inspirehep.curation.search_check_do import SearchCheckDo
from inspire_utils.record import get_value
import datetime
from itertools import chain


DATE_BEFORE_2023 = datetime.datetime.strptime("2023", "%Y")


class RemoveQuantPh(SearchCheckDo):
    """Remove core from quant-ph literature records"""

    query = "arxiv_eprints.categories:quant-ph core:true not _desy_bookkeeping.status:final not _desy_bookkeeping.status:printed and de < 2023"

    @staticmethod
    def check(record, logger, state):
        arxiv_category_quant_ph = "quant-ph" in chain.from_iterable(
            get_value(record, "arxiv_eprints.categories", [])
        )
        is_core = record.get("core")
        desy_bookkeeping_not_final = "final" not in record.get(
            "_desy_bookkeeping.status", []
        )
        desy_bookkeeping_status_not_printed = "printed" not in get_value(
            record, "_desy_bookkeeping.status", []
        )
        earliest_date_before_2023 = (
            datetime.datetime.strptime(record.earliest_date, "%Y-%m-%d")
            < DATE_BEFORE_2023
        )
        return all(
            [
                arxiv_category_quant_ph,
                is_core,
                desy_bookkeeping_not_final,
                desy_bookkeeping_status_not_printed,
                earliest_date_before_2023,
            ]
        )

    @staticmethod
    def do(record, logger, state):
        del record["core"]


RemoveQuantPh()
