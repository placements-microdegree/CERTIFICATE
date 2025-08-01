#!/usr/bin/env python3
"""
Simple Supabase Test
"""

import os

# Set environment variables directly
os.environ["SUPABASE_URL"] = "https://wyszrjhxucxblyvhrktn.supabase.co"
os.environ["SUPABASE_KEY"] = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw"
)

print("🔍 Testing Supabase connection...")

try:
    from supabase import create_client, Client

    # Initialize Supabase client
    supabase: Client = create_client(
        os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"]
    )

    print("✅ Supabase client created successfully!")

    # Test connection by trying to access a table
    try:
        response = supabase.table("certificates").select("*").limit(1).execute()
        print("✅ Connected to Supabase database!")
        print(f"📊 Found {len(response.data)} certificates")

        if len(response.data) == 0:
            print("📝 Adding sample data...")
            sample_data = {
                "certificate_id": "MD-12345678",
                "student_name": "Habin Rahman",
                "course_name": "Advanced Python Programming",
                "completion_date": "2024-01-15",
                "certificate_url": "https://cert.microdegree.work/cert/MD-12345678",
            }
            supabase.table("certificates").insert(sample_data).execute()
            print("✅ Sample data added!")

        print("\n🎉 Supabase integration is working!")
        print("Your Flask app is now connected to Supabase!")

    except Exception as e:
        print(f"❌ Database error: {e}")
        print("💡 Make sure you have created the 'certificates' table in Supabase!")

except Exception as e:
    print(f"❌ Connection error: {e}")
