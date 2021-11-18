from inspirehep.curation.search_check_do import SearchCheckDo


class AddToFermilabCollection(SearchCheckDo):
    '''Add records with Fermilab report numbers to the Fermilab collection.'''

    query = 'r FERMILAB* -_collections:Fermilab'

    @staticmethod
    def check(record, logger, state):
        reports = record.get_value('report_numbers.value', [])
        logger.info("Report numbers in record", reports=reports)
        return any(
            report.lower.startswith('fermilab') for report in reports
        )

    @staticmethod
    def do(record, logger, state):
        _collections.append('Fermilab')

AddToFermilabCollection()
