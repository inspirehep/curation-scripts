from inspirehep.curation.search_check_do import SearchCheckDo
from inspire_dojson.utils import get_recid_from_ref
from inspire_utils.record import get_value


AFFECTED_AUTHORS_RECIDS = {
    2170881,
    2165762,
    2171911,
    2167309,
    2166287,
    2166288,
    2166290,
    2169364,
    2168854,
    2168855,
    2166296,
    2167322,
    2166300,
    2166302,
    2166303,
    2174501,
    2167346,
    2168891,
    2165821,
    2168387,
    2172506,
    2023003,
    2169948,
    2169436,
    2169438,
    2168417,
    2169441,
    2169444,
    2169445,
    2169961,
    2169962,
    2169963,
    2169964,
    2169965,
    2169967,
    2169968,
    2169969,
    2169970,
    2169971,
    1116790,
    2174586,
    2174587,
    2174588,
    2174589,
    2174590,
    2174591,
    2164361,
    2165391,
    2163865,
    1933467,
    2172577,
    2164389,
    2172582,
    2164391,
    2172584,
    2172583,
    2164390,
    2165420,
    2164405,
    2163896,
    2169029,
    2164433,
    2164464,
    2173170,
    2164466,
    2164468,
    2164470,
    2164471,
    2164472,
    2164473,
    2164474,
    2165509,
    2165511,
    2171149,
    2171151,
    2165535,
    2165538,
    2173219,
    2165540,
    2165541,
    2165542,
    2172712,
    2172713,
    2173744,
    2173747,
    2165556,
    2173748,
    2165559,
    2165560,
    2173754,
    2165562,
    2165564,
    2165566,
    2165568,
    2165569,
    2165570,
    2173763,
    2163010,
    2173765,
    2165575,
    2165576,
    2173769,
    2173775,
    2173777,
    2173779,
    2173780,
    2168661,
    2174810,
    2173787,
    2174812,
    2173789,
    2173791,
    2173794,
    2169194,
    2165108,
    2165109,
    2165120,
    2166659,
    2164612,
    2164615,
    2173323,
    2165135,
    2163610,
    2171293,
    2172830,
    2167209,
    2163118,
    2170810,
    2172861,
    2172863,
    2172864,
    2172865,
    2163135,
    2163149,
    2173902,
    2163150,
    2163151,
    2173901,
    2163668,
    2169301,
    2169302,
    2167769,
    2168797,
    2168799,
    2167776,
    2167777,
    2167779,
    2166249,
    2167274,
    2167275,
    2172908,
    2167276,
    2167293,
}


class FixLinkedNonexistentAuthors(SearchCheckDo):
    """Remove ref from authors linked to nonexisting profiles."""

    query = {
        "query": {
            "nested": {
                "path": "authors",
                "query": {
                    "terms": {"authors.record.$ref": list(AFFECTED_AUTHORS_RECIDS)}
                },
            }
        }
    }

    def search(self):
        self.logger.info("Searching records", query=self.query)
        query = (
            self.search_class()
            .from_dict(self.query)
            .params(_source={}, size=self.size, scroll="60m")
        )
        if shard_filter := self._current_shard_filter():
            query = query.filter("script", script=shard_filter)
        return query.scan()

    @staticmethod
    def check(record, logger, state):
        refs = get_value(record, "authors.record", [])
        journal_recids_record = {int(get_recid_from_ref(ref)) for ref in refs}
        return AFFECTED_AUTHORS_RECIDS.intersection(journal_recids_record)

    @staticmethod
    def do(record, logger, state):
        for author in record.get("authors", []):
            if "record" not in author:
                continue
            recid = get_recid_from_ref(author["record"].to_dict())
            if int(recid) in AFFECTED_AUTHORS_RECIDS:
                del author["record"]


FixLinkedNonexistentAuthors()
