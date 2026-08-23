def build_delivery_row(raw, ai, sku):

    return {
        "SKU": sku,
        "Manufacturer Part Number": ai["Manufacturer Part Number"],
        "Product Name": ai["Product Name"],
        "Brand": ai["Brand"],
        "Manufacturer": ai["Manufacturer"],
        "Category": ai["Category"],
        "Subcategory": ai["Subcategory"],
        "Description": ai["Description"],
        "Material": ai["Material"],
        "Dimensions": ai["Dimensions"],
        "Country of Origin": ai["Country of Origin"],
        "HS Code": ai["HS Code"],
        "Confidence Score": ai["Confidence Score"]
    }

def build_audit_row(raw, ai, error, latency):

    return {
        "Part Number": raw["Mfg_Part_Num"],
        "Original Description": raw["Part_Desc"],
        "Predicted Brand": ai["Brand"],
        "Predicted Category": ai["Category"],
        "Confidence": ai["Confidence Score"],
        "Source": "AI + Product Description",
        "Latency": latency,
        "Status": "Validated"
    }