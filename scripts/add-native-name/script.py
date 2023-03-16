import re
from nameparser import HumanName
from inspirehep.curation.search_check_do import SearchCheckDo

CHINESE_NAME = re.compile(r'[\u4e00-\u9fff]+', re.UNICODE)

class AddNativeName(SearchCheckDo):
    '''Add records with Fermilab report numbers to the Fermilab collection.'''

    query = '-name.native_names:* _collections:Authors'

    @staticmethod
    def check(record, logger, state):
        name_dict = record.get_value('name', {})
        logger.info("Names in record", name_dict=name_dict)
        if 'native_names' in name_dict:
            return False
        return CHINESE_NAME.search(name_dict['value'])


    @staticmethod
    def do(record, logger, state):
        name_dict = record.get_value('name', {})
        name = name_dict['value']
        native_name = CHINESE_NAME.search(name).group(0)
        name = re.sub(native_name, '', name)
        name = HumanName(name)
        name = f'{name.surnames}, {name.first}'
        name = re.sub(r'[ ]+\,', ',', name)
        name_dict['value'] = name
        name_dict['native_names'] = native_name


AddNativeName()
