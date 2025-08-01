#!/usr/bin/env python3
"""
Test script to verify Supabase connection
"""

from supabase_config import supabase, get_all_certificates


def test_supabase_connection():
    """Test the Supabase connection"""
    print("Testing Supabase connection...")

    if supabase:
        print("✅ Supabase client initialized successfully")

        # Test fetching all certificates
        try:
            certificates = get_all_certificates()
            print(
                f"✅ Successfully fetched {len(certificates)} certificates from database"
            )

            if certificates:
                print("Sample certificate data:")
                for cert in certificates[:2]:  # Show first 2 certificates
                    print(f"  - ID: {cert.get('certificate_id')}")
                    print(f"    Name: {cert.get('student_name')}")
                    print(f"    Course: {cert.get('course_name')}")
                    print()
            else:
                print("No certificates found in database")

        except Exception as e:
            print(f"❌ Error fetching certificates: {e}")
    else:
        print("❌ Supabase client not initialized")


if __name__ == "__main__":
    test_supabase_connection()
