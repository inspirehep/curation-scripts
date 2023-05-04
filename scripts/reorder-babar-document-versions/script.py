import re

from inspirehep.curation.search_check_do import SearchCheckDo


def key_func(document):
    description = document.get("description", "")
    match = re.match(r"\[Version (\d+(.\d+))\]", description)
    if match:
        return ("", float(match.group(1)))
    else:
        return (description, 0)


class ReorderBabarDocumentVersions(SearchCheckDo):
    """Order the documents in the Babar collections according to versions."""

    query = "documents.description:version and _collections:babar analysis documents"

    @staticmethod
    def check(record, logger, state):
        documents = record.get("documents", [])
        state["sorted"] = sorted(documents, key=key_func)
        return state["sorted"] != documents

    @staticmethod
    def do(record, logger, state):
        record["documents"] = state["sorted"]


ReorderBabarDocumentVersions()
