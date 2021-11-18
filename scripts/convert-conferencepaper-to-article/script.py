from inspirehep.curation.search_check_do import SearchCheckDo

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


class ConvertConferencePapertoArticle(SearchCheckDo):
    """SIF Conferences have no Proceedings, convert to regular articles"""

    query = " or ".join(["publication_info.cnum:%s" % cnum for cnum in cnums])

    @staticmethod
    def check(record, logger, state):
        # process records with given CNUM
        # dont process other CNUMs
        # dont process proceedings

        state["pos_cnum"] = []
        if "proceedings" in record["document_type"]:
            return False
        for npbn, pbn in enumerate(record.get("publication_info", [])):
            cnum = pbn.get("cnum", "")
            if cnum in cnums:
                state["pos_cnum"].append(npbn)
            elif cnum:
                return False
        if state["pos_cnum"]:
            return True
        return False

    @staticmethod
    def do(record, logger, state):
        # remove CNUM and conference record
        # remove doc_type conference paper
        # add doc_type article
        # add refereed
        for npbn in state["pos_cnum"]:
            record["publication_info"][npbn].pop("cnum", "")
            record["publication_info"][npbn].pop("conference_record", "")

        if "conference paper" in record["document_type"]:
            record["document_type"].remove("conference paper")
        if not "article" in record["document_type"]:
            record["document_type"].append("article")
        record["refereed"] = True


ConvertConferencePapertoArticle()
