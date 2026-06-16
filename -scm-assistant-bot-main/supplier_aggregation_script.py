
import pandas as pd

df = pd.read_csv("supplier_performance_data.csv")

supplier_docs = []

for supplier_id, g in df.groupby("Supplier_ID"):
    supplier_name = g["Supplier_Name"].iloc[0]

    disruptions = sorted(
        set(str(x).strip() for x in g["Active_Disruptions"].dropna().unique())
    )

    certifications = sorted(
        set(";".join(g["Certifications"].fillna("")).split(";"))
    )
    certifications = [c for c in certifications if c]

    doc = f"""
Supplier_ID: {supplier_id}
Supplier_Name: {supplier_name}

Region: {g['Region'].iloc[0]}
Country: {g['Country'].iloc[0]}

Contract_Tier: {g['Contract_Tier'].iloc[0]}
Risk_Level: {g['Risk_Level'].iloc[0]}

Compliance_Score_Avg: {round(g['Compliance_Score'].mean(),2)}
Sustainability_Score_Avg: {round(g['Sustainability_Score'].mean(),2)}

Average_OTD: {round(g['OTD_Rate_Pct'].mean(),2)}
Average_Defect_Rate: {round(g['Defect_Rate_Pct'].mean(),2)}

PO_Count: {len(g)}
Total_PO_Value_USD: {round(g['PO_Value_USD'].sum(),2)}

Units_Ordered_Total: {int(g['Units_Ordered'].sum())}
Units_Delivered_Total: {int(g['Units_Delivered_On_Time'].sum())}
Units_Rejected_Total: {int(g['Units_Rejected'].sum())}

Active_Disruptions:
{", ".join(disruptions) if disruptions else "None"}

Certifications:
{", ".join(certifications)}
"""
    supplier_docs.append(doc)

with open("supplier_profiles.txt", "w", encoding="utf-8") as f:
    f.write("\n\n=============================\n\n".join(supplier_docs))

print(f"Generated {len(supplier_docs)} supplier profiles")
