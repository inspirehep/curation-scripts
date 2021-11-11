from inspirehep.curation.search_check_do import SearchCheckDo


class RemovePDFAExtension(SearchCheckDo):
    """Remove ``;pdfa`` extension from filenames as it messes up CDS display."""

    query = "documents.filename:*pdfa"

    @staticmethod
    def check(record, logger, state):
        return any(
            f.endswith(";pdfa") for f in record.get_value("documents.filename", [])
        )

    @staticmethod
    def do(record, logger, state):
        extension = ";pdfa"
        for document in record["documents"]:
            if (filename := document.get("filename", "")).endswith(extension):
                document["filename"] = filename[: len(extension)]


RemovePDFAExtension()
