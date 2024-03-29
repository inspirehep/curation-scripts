from inspirehep.curation.search_check_do import SearchCheckDo

wrong_cnum = "C20-05-18.1"
new_cnum = "C21-05-31"
new_conf_record = "https://inspirehep.net/api/conferences/1812458"


class ChangeCNUM(SearchCheckDo):
    """Wrong CNUM assigned - replace by correct information"""

    query = "publication_info.cnum:%s" % wrong_cnum

    @staticmethod
    def check(record, logger, state):
        # flag PBN with wrong CNUM

        state["pos_cnum"] = []
        for npbn, pbn in enumerate(record.get("publication_info", [])):
            cnum = pbn.get("cnum", "")
            if cnum == wrong_cnum:
                state["pos_cnum"].append(npbn)
        if state["pos_cnum"]:
            return True
        return False

    @staticmethod
    def do(record, logger, state):
        # replace CNUM and conference record

        for npbn in state["pos_cnum"]:
            record["publication_info"][npbn]["cnum"] = new_cnum
            record["publication_info"][npbn]["conference_record"] = (
                "{'$ref': '%s'}" % new_conf_record
            )


ChangeCNUM()
