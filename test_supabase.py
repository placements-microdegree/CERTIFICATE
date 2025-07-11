#!/usr/bin/env python3
"""
Test Supabase Connection
"""

import os

# Set environment variables
os.environ['SUPABASE_URL'] = 'https://wyszrjhxucxblyvhrktn.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5c3pyamh4dWN4Ymx5dmhya3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4OTAzNzgsImV4cCI6MjA2NzQ2NjM3OH0.ZEPZIXsIVXbor8vY1uJM9VVVnody5iDJOgabbov14Xw'

try:
    from supabase_config import get_all_certificates, add_sample_data
    
    print("🔍 Testing Supabase connection...")
    
    # Test connection
    certificates = get_all_certificates()
    print(f"✅ Connected to Supabase!")
    print(f"📊 Found {len(certificates)} certificates in database")
    
    # Add sample data if no certificates exist
    if len(certificates) == 0:
        print("📝 Adding sample certificate data...")
        add_sample_data()
        print("✅ Sample data added successfully!")
    else:
        print("📋 Sample data already exists!")
    
    print("\n🎉 Supabase integration is working!")
    print("=" * 50)
    print("Your app is now using Supabase database!")
    print("\n📋 Test URLs:")
    print("- Verification Portal: http://localhost:5000/")
    print("- Certificate Template: http://localhost:5000/cert/MD-12345678")
    print("- API Endpoint: http://localhost:5000/certificates/MD-12345678")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Make sure you have created the 'certificates' table in Supabase!") 