from inspirehep.curation.search_check_do import SearchCheckDo

ECONF_URL = 'https://www.slac.stanford.edu/econf/C210711/'
ECONF_DESCRIPTION = 'eConf'
ECONF_CNUM = 'C21-07-11'


class AddSnowmassProceedingsURL(SearchCheckDo):
    '''Add link to the Snowmass eConf Proceedings website.'''


    query = f'publication_info.cnum:{ECONF_CNUM}'
    query += f' -urls.description:{ECONF_DESCRIPTION}'

    @staticmethod
    def check(record, logger, state):
        urls = record.get_value('urls.description', [])
        logger.info('URLs in record', urls=urls)
        if ECONF_DESCRIPTION in urls:
            return False
        cnums = record.get_value('publication_info.cnum', [])
        return ECONF_CNUM in cnums

    @staticmethod
    def do(record, logger, state):
        record.setdefault("urls", []).append({
            "value": ECONF_URL,
            "description": ECONF_DESCRIPTION,
        })


AddSnowmassProceedingsURL()
