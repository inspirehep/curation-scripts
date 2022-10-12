import re

from dojson.contrib.marc21.utils import create_record
from invenio_pidstore.models import PersistentIdentifier
from inspire_dojson.utils import force_list
from inspire_utils.dedupers import dedupe_list
from inspirehep.curation.search_check_do import SearchCheckDo
from inspirehep.migrator.models import LegacyRecordsMirror
from inspirehep.records.utils import get_ref_from_pid
from inspirehep.search.api import LiteratureSearch, IQ

BABAR_COLLECTIONS = [
    "BaBar Analysis Documents",
    "BaBar Internal notes",
    "BaBar Internal BAIs",
]


def get_legacy_relations(recid):
    record = LegacyRecordsMirror.query.get(recid)
    if not record:
        return None
    legacy_rec = create_record(record.marcxml)
    legacy_relations = force_list(legacy_rec.get("78708"))
    return [
        (relation.get("i", "").strip(), relation.get("r", "").strip())
        for relation in legacy_relations
    ]


def find_report_numbers(report_number):
    clean_report_number = re.sub(r"\[.*\]", "", report_number).strip()
    search_instance = LiteratureSearch()
    query = search_instance.query(
        IQ(f'report_numbers.value.fuzzy:"{clean_report_number}"', search_instance)
    ).params(size=2)
    result = query.execute()
    uuids = [r.meta.id for r in result]
    pids = PersistentIdentifier.query.filter(
        PersistentIdentifier.object_uuid.in_(uuids),
        PersistentIdentifier.object_type == "rec",
        PersistentIdentifier.pid_type == "lit",
    ).all()
    return [get_ref_from_pid(pid.pid_type, pid.pid_value) for pid in pids]


class RestoreBabarRelatedRecords(SearchCheckDo):
    """Restore ``related_records`` in BaBar records that got lost in migration."""

    query = " or ".join([f'_collections:"{coll}"' for coll in BABAR_COLLECTIONS])

    @staticmethod
    def check(record, logger, state):
        state["legacy_relations"] = get_legacy_relations(record["control_number"])
        if not state["legacy_relations"]:
            logger.warning("No legacy record found")
            return False

        return bool(state["legacy_relations"])

    @staticmethod
    def do(record, logger, state):
        legacy_relations = state["legacy_relations"]
        related_records = record.get("related_records", [])
        urls = record.get("urls", [])
        for description, report_number in legacy_relations:
            matched_recs = find_report_numbers(report_number)
            if not matched_recs:
                logger.warning(
                    "No records found for report number", report_number=report_number
                )
                continue
            elif (num_matches := len(matched_recs)) > 1:
                logger.warning(
                    "Multiple records found for report number",
                    report_number=report_number,
                    num_matches=num_matches,
                )
                continue
            related_records.append(
                {
                    "relation_freetext": description,
                    "record": matched_recs[0],
                    "curated_relation": True,
                }
            )
            urls.append(
                {
                    "value": matched_recs[0]["$ref"].replace("/api", ""),
                    "description": report_number,
                }
            )
        if related_records:
            record["related_records"] = dedupe_list(related_records)
        if urls:
            record["urls"] = dedupe_list(urls)


RestoreBabarRelatedRecords()
