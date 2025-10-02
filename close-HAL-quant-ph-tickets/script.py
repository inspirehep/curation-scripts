from inspirehep.curation.search_check_do import SearchCheckDo
from inspirehep.snow.api import InspireSnow


class CloseHALQuantPhTickets(SearchCheckDo):
    """Close HAL tickets created during the quant-ph backlog reharvest."""

    query = "arxiv_eprints.categories:quant-ph and da >= 2025-09-28 and not arxiv_eprints.value:25*"

    @staticmethod
    def check(record, logger, state):
        tickets = InspireSnow().get_tickets_by_recid(record["control_number"])
        for ticket in tickets:
            if ticket["u_functional_category"] == "HAL curation":
                InspireSnow().resolve_ticket(ticket["sys_id"])
                logger.info("Resolved SNOW ticket.")
        # No need to do anything on the record itself
        return False

    @staticmethod
    def do(record, logger, state):
        pass


CloseHALQuantPhTickets()

