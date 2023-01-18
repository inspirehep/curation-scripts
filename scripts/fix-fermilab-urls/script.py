import requests

from inspirehep.curation.search_check_do import SearchCheckDo

FIXED_URLS = requests.get(
    "https://cernbox.cern.ch/remote.php/dav/public-files/"
    "FVgeaG5VAVx8B09/fermilab_fixed_urls.json"
).json()

class FixFermilabURLs(SearchCheckDo):
    """Rewrite URLs to Fermilab PDFs that have moved."""

    query = "urls.value:'ccd.fnal.gov'"

    @staticmethod
    def check(record, logger, state):
        for url in record.get_value("urls.value", []):
            if "ccd.fnal.gov" not in url:
                continue
            if url in FIXED_URLS:
                return True
            logger.warning("URL not found in translation map", url=url)
        return False

    @staticmethod
    def do(record, logger, state):
        for url in record["urls"]:
            value = url["value"]
            if "ccd.fnal.gov" in value:
                url["value"] = FIXED_URLS.get(value, value)


FixFermilabURLs()

