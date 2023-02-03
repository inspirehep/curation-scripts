from itertools import chain
from inspirehep.curation.search_check_do import SearchCheckDo
from inspire_schemas.utils import is_arxiv, normalize_arxiv


class FixArxivRefs(SearchCheckDo):
    """Identify arXiv references in DOIs and URLs."""

    query = (
        "references.reference.dois:10.48550* "
        "or references.reference.urls.value:'arxiv' "
        "or references.reference.urls.value:'arXiv' "
        "or references.reference.urls.value:'ARXIV'"
    )

    @staticmethod
    def check(record, logger, state):
        dois = chain.from_iterable(record.get_value("references.reference.dois"))
        urls = chain.from_iterable(record.get_value("references.reference.urls.value"))
        return any("arxiv" in val.lower() for val in chain(dois, urls))

    @staticmethod
    def do(record, logger, state):
        for reference in record("references"):
            reference = reference.get("reference", {})

            if "arxiv_eprint" in reference:
                continue

            new_dois = []
            for doi in reference.get("dois", []):
                if is_arxiv(doi):
                    reference["arxiv_eprint"] = normalize_arxiv(doi)
                else:
                    new_dois.append(doi)
            if new_dois:
                reference["dois"] = new_dois
            else:
                reference.pop("dois", None)

            new_urls = []
            for url in reference.get("urls", []):
                if is_arxiv(url["value"]):
                    reference["arxiv_eprint"] = normalize_arxiv(url["value"])
                else:
                    new_urls.append(url)
            if new_urls:
                reference["urls"] = new_urls
            else:
                reference.pop("urls", None)


FixArxivRefs()
