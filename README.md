"""
mapping.py
----------
Maps an EnrichmentResult (Claude's structured JSON) + the original sparse
input row onto the EXACT 252-column delivery schema from schema.py.

Columns with no reliable source (images, PDFs, UPC/GTIN, pricing, physical
dimensions, ref URLs, etc.) are intentionally left as empty strings - see
enrichment_engine.py docstring for why that's a deliberate design choice,
not an oversight.
"""

from schema import EXPECTED_HEADERS


def build_delivery_row(row_input: dict, ai: dict, sku_seed: int) -> dict:
    """Return a dict keyed by EXPECTED_HEADERS for one product."""
    out = {h: "" for h in EXPECTED_HEADERS}

    cls = ai.get("classification", {})
    brand = ai.get("brand", {})
    desc = ai.get("descriptions", {})
    features = ai.get("features", [])
    attrs = ai.get("attributes", [])

    out["PART_NUMBER"] = str(sku_seed)
    out["Dept"] = cls.get("dept", "")
    out["Class"] = cls.get("class_", "")
    out["Fine"] = cls.get("fine", "")
    out["SKU - MY_PART_NUMBER"] = str(sku_seed)

    # pass-through original input columns (schema keeps these verbatim)
    out["Mfg_Part_Num"] = row_input.get("Mfg_Part_Num", "")
    out["Part_Desc"] = row_input.get("Part_Desc", "")
    out["E1_Brand"] = row_input.get("E1_Brand", "")
    out["Unilog_Brand"] = row_input.get("Unilog_Brand", "")
    out["DIB_Brand"] = row_input.get("DIB_Brand", "")
    out["Part_Manuf"] = row_input.get("Part_Manuf", "")

    out["MANUFACTURER_NAME"] = brand.get("manufacturer_name", "")
    out["BRAND_NAME"] = brand.get("brand_name", "")
    out["TRADE_NAME"] = brand.get("trade_name", "")
    out["MANUFACTURER_PART_NUMBER"] = row_input.get("Mfg_Part_Num", "")
    out["Classpath"] = cls.get("classpath", "")

    out["MOBILE_DESC"] = desc.get("mobile_desc", "")
    out["INVOICE_DESC"] = desc.get("invoice_desc", "")
    out["SHORT_DESC"] = desc.get("short_desc", "")
    out["LONG_DESC1"] = desc.get("long_desc1", "")
    out["RETAIL_DESC"] = desc.get("retail_desc", "")
    out["MARKETING_DESCRIPTION"] = desc.get("marketing_description", "")

    for i, feat in enumerate(features[:20], start=1):
        out[f"ITEM_FEATURES_{i}"] = feat

    for i, a in enumerate(attrs[:50], start=1):
        out[f"ATTRIBUTE_LABEL {i}"] = a.get("label", "")
        out[f"ATTRIBUTE_VALUE {i}"] = a.get("value", "")
        out[f"ATTRIBUTE_UOM {i}"] = a.get("uom", "")

    out["UNSPSC"] = cls.get("unspsc_guess", "")
    out["Country Of Origin"] = ai.get("country_of_origin", "")

    return out


def build_audit_row(row_input: dict, ai: dict, error: str | None, latency_s: float) -> dict:
    conf = ai.get("confidence", {}) if ai else {}
    return {
        "Mfg_Part_Num": row_input.get("Mfg_Part_Num", ""),
        "status": "error" if error else "ok",
        "error": error or "",
        "latency_s": round(latency_s, 2),
        "confidence_classification": conf.get("classification", ""),
        "confidence_brand": conf.get("brand", ""),
        "confidence_descriptions": conf.get("descriptions", ""),
        "confidence_attributes": conf.get("attributes", ""),
        "reasoning": ai.get("reasoning", "") if ai else "",
        "validation_flags": " | ".join(ai.get("validation_flags", [])) if ai else "",
    }
