from inspirehep.curation.search_check_do import SearchCheckDo

tag_info = ("parent_isbn", "9789811947506")

missing_info = {
    "journal_title": "Springer Proc.Math.Stat.",
    "journal_volume": "396",
    "parent_record": {"$ref": "https://inspirehep.net/api/literature/2628642"},
}


class AmendPBN(SearchCheckDo):
    """Add missing info to PBNs with tag"""

    query = "publication_info.%s:%s" % tag_info

    @staticmethod
    def check(record, logger, state):
        # flag PBN containing tag info

        state["pos_tag"] = []
        for npbn, pbn in enumerate(record.get("publication_info", [])):
            tag = pbn.get("tag_info(0)", "")
            if tag == tag_info(1):
                state["pos_tag"].append(npbn)
        if state["pos_tag"]:
            return True
        return False

    @staticmethod
    def do(record, logger, state):
        # append missing info

        for npbn in state["pos_tag"]:
            for key, value in missing_info.items():
                record["publication_info"][npbn][key] = value


AmendPBN()
