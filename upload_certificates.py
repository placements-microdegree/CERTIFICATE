import pandas as pd
from supabase import create_client, Client

# Supabase credentials (replace with yours)

# Load CSV
df = pd.read_csv("AWS Live Certification  (Responses) - Form Responses 1 (2).csv")

# Keep only the required columns
df = df[["Timestamp", "Certificate No", "Full Name", "Batch  (eg : AWS-Batch-E-02032022) "]]

# Insert into Supabase
for _, row in df.iterrows():
    certificate_id = row["Certificate No"] if pd.notna(row["Certificate No"]) else None
    data = {
        "completion_date": row["Timestamp"],
        "certificate_id": certificate_id,
        "student_name": row["Full Name"],
        "course_name": row["Batch  (eg : AWS-Batch-E-02032022) "],
        "certificate_url": f"/cert/{certificate_id}" if certificate_id else None
    }
    supabase.table("certificates").insert(data).execute()

print("✅ Upload completed!")
