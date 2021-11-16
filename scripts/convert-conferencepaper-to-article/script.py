from inspirehep.curation.search_check_do import SearchCheckDo


class ConvertConferencePapertoArticle(SearchCheckDo):
    """SIF Conferences have no Proceedings, convert to regular articles"""

    cnums = [
        "C20-09-14.4",
        "C19-09-23.10",
        "C18-09-17.9",
        "C17-09-11.10",
        "C16-09-26.2",
        "C14-09-22.10",
        "C13-09-23.8",
        "C12-09-17.11",
        "C11-09-26.11",
    ]
    query = " or ".join(["publication_info.cnum:%s" % cnum for cnum in cnums])

    @staticmethod
    def check(record, logger, state):
        if "proceedings" in record["document_type"]:
            return False
        for npbn, pbn in enumerate(record.get("publication_info", [])):
            if pbn.get("cnum", "") in cnums:
                state["pos_cnum"] = npbn
                return True
        return False

    @staticmethod
    def do(record, logger, state):
        record["publication_info"][state["pos_cnum"]].pop("cnum", "")
        record["publication_info"][state["pos_cnum"]].pop("conference_record", "")

        if "conference paper" in record["document_type"]:
            record["document_type"][
                record["document_type"].index("conference paper")
            ] = "article"
        record["refereed"] = True


ConvertConferencePapertoArticle()
