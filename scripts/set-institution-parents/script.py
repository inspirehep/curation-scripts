# mapping INDIAN institutions to their parent institutions, as per the mapping source

from inspirehep.curation.search_check_do.base import SearchCheckDo
from inspirehep.records.utils import get_ref_from_pid
from inspirehep.search.api import InstitutionsSearch

# Mapping source — hardcoded
CHILD_TO_PARENT = {
    903134: 2794753,
    903329: 1742673,
    903457: 1342995,
    903464: 1267133,
    903467: 1302872,
    903479: 909622,
    903616: 909554,
    903618: 1252948,
    903780: 1238876,
    903997: 1265037,
    904436: 905389,
    905927: 911113,
    906500: 902873,
    907561: 906476,
    907589: 904167,
    907637: 910947,
    907924: 902975,
    908148: 902658,
    908329: 902767,
    908468: 903676,
    908581: 1342995,
    908645: 914863,
    908667: 910871,
    908976: 904610,
    909746: 902767,
    910199: 911283,
    910947: 907637,
    911113: 905927,
    911157: 912497,
    911389: 903809,
    911575: 904006,
    911617: 1388778,
    911618: 902767,
    911812: 906566,
    911897: 2857180,
    912008: 3170799,
    912381: 903456,
    914887: 903933,
    1120890: 903253,
    1120891: 903253,
    1120892: 903253,
    1128166: 911554,
    1208785: 911767,
    1265989: 1302872,
    1267119: 2842390,
    3170800: 911767,
}

class SetInstitutionParents(SearchCheckDo):

    search_class = InstitutionsSearch
    query = "addresses.country_code:IN"
 
    @staticmethod
    def check(record, logger, state):
        control_number = record.get("control_number")
 
        if control_number not in CHILD_TO_PARENT:
            return False
 
        parent_cn = CHILD_TO_PARENT[control_number]

        # skip records whose parent is itself to avoid corrupting related_records.
        if control_number == parent_cn:
            logger.warning(
                "Skipping: control_number equals its own listed parent",
                control_number=control_number,
            )
            return False
 
        # skip if the exact parent link already exists and ICN is already ['obsolete'].
        existing_parent_refs = [
            r.get("record", {})
            for r in record.get("related_records", [])
            if r.get("relation") == "parent"
        ]

        wanted_ref = get_ref_from_pid("ins", parent_cn)
        already_linked = existing_parent_refs == [wanted_ref]
        already_obsolete = record.get("ICN") == ["obsolete"]
        if already_linked and already_obsolete:
            return False
 
        return True
 
    @staticmethod
    def do(record, logger, state):
        parent_cn = CHILD_TO_PARENT[record.get("control_number")]
 
        # 1. related_records: replace any existing parent link, keep
        #    everything else (e.g. "predecessor" relations) untouched
        existing = record.get("related_records", [])
        kept = [r for r in existing if r.get("relation") != "parent"]
        old_parents = [r for r in existing if r.get("relation") == "parent"]
        if old_parents:
            logger.warning(
                "Replacing existing parent relation(s)",
                control_number=record.get("control_number"),
                old_parent_refs=[r.get("record", {}) for r in old_parents],
                new_parent_control_number=parent_cn,
            )
 
        record["related_records"] = kept + [
            {
                "relation": "parent",
                "record": get_ref_from_pid("ins", parent_cn),
            }
        ]
 
        # 2. ICN: mark the child as obsolete now that it's linked to its parent
        old_icn = record.get("ICN", [])
        if old_icn and old_icn != ["obsolete"]:
            logger.warning(
                "Replacing existing ICN with ['obsolete']",
                control_number=record.get("control_number"),
                old_icn=old_icn,
            )
        record["ICN"] = ["obsolete"]
 
 
SetInstitutionParents()