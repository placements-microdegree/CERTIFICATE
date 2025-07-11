#!/usr/bin/env python3
"""
Add sample certificate data to Supabase
"""

from supabase_config import supabase

def add_sample_data():
    """Add sample certificate data to Supabase"""
    if not supabase:
        print("❌ Supabase client not initialized")
        return
        
    sample_certificates = [
        {
            "certificate_id": "MD-12345678",
            "student_name": "Habin Rahman",
            "course_name": "Advanced Python Programming",
            "completion_date": "2024-01-15",
            "certificate_url": "https://cert.microdegree.work/cert/MD-12345678"
        },
        {
            "certificate_id": "MD-87654321",
            "student_name": "Sarah Johnson",
            "course_name": "Web Development Fundamentals",
            "completion_date": "2024-02-20",
            "certificate_url": "https://cert.microdegree.work/cert/MD-87654321"
        },
        {
            "certificate_id": "MD-11223344",
            "student_name": "Michael Chen",
            "course_name": "Data Science Essentials",
            "completion_date": "2024-03-10",
            "certificate_url": "https://cert.microdegree.work/cert/MD-11223344"
        }
    ]
    
    try:
        for cert in sample_certificates:
            supabase.table('certificates').insert(cert).execute()
        print("✅ Sample data added successfully!")
        print(f"Added {len(sample_certificates)} certificates to database")
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

if __name__ == "__main__":
    add_sample_data() 