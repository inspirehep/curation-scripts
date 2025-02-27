from itertools import chain

from inspirehep.curation.search_check_do import SearchCheckDo

INSTITUTIONS = {
    "2020952",
    "903118",
    "1188219",
    "907607",
    "1201986",
    "904493",
    "1347082",
    "1776404",
    "902828",
    "911366",
    "1743848",
    "902740",
    "902786",
    "903119",
    "902989",
    "903421",
    "1776405",
    "910133",
    "902703",
    "906885",
    "903453",
    "907247",
    "911249",
    "1608212",
    "903100",
    "907588",
    "903099",
    "902974",
}


class FlagExportToHAL(SearchCheckDo):
    """Enable export to HAL for a bunch of unflagged records."""

    query = (
        'jy 2016 and (document_type:"conference paper" or document_type:"article") '
        "and not _export_to.HAL:true and _collections:Literature "
        f"and affid:{';'.join(INSTITUTIONS)} and external_system_identifiers.schema:HAL"
    )

    @staticmethod
    def check(record, logger, state):
        has_correct_pubyear = 2016 in record.get_value("publication_info.year", [])
        has_correct_doctype = (
            "conference paper" in record["document_type"]
            or "article" in record["document_type"]
        )
        has_correct_external_identifier = "HAL" in record.get_value(
            "external_system_identifiers.schema", []
        )
        has_correct_affiliations = any(
            aff_ref.split("/")[-1] in INSTITUTIONS
            for aff_ref in chain.from_iterable(
                record.get_value("authors.affiliations.record.$ref", [])
            )
        )

        return (
            has_correct_pubyear
            and has_correct_doctype
            and has_correct_external_identifier
            and has_correct_affiliations
        )

    @staticmethod
    def do(record, logger, state):
        record.setdefault("_export_to", {})["HAL"] = True


FlagExportToHAL()
