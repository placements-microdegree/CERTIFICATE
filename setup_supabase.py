#!/usr/bin/env python3
"""
Supabase Setup Script for Certificate Verification App
"""

import os
from supabase_config import add_sample_data


def setup_supabase():
    """Setup Supabase configuration"""
    print("🔧 Setting up Supabase for Certificate Verification App")
    print("=" * 50)

    # Get Supabase credentials
    print("\n📋 Please provide your Supabase credentials:")

    supabase_url = input(
        "Enter your Supabase URL (e.g., https://your-project.supabase.co): "
    ).strip()
    supabase_key = input("Enter your Supabase anon key: ").strip()

    if not supabase_url or not supabase_key:
        print("❌ Error: Both URL and key are required!")
        return

    # Create .env file
    env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""

    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file with Supabase credentials")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

    # Test connection
    print("\n🔍 Testing Supabase connection...")
    os.environ["SUPABASE_URL"] = supabase_url
    os.environ["SUPABASE_KEY"] = supabase_key

    try:
        from supabase_config import get_all_certificates

        certificates = get_all_certificates()
        print("✅ Successfully connected to Supabase!")
        print(f"📊 Found {len(certificates)} certificates in database")
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return

    # Add sample data
    print("\n📝 Adding sample certificate data...")
    add_sample_data()

    print("\n🎉 Setup complete!")
    print("=" * 50)
    print("Your app is now configured to use Supabase!")
    print("\n📋 Next steps:")
    print("1. Run: python app.py")
    print("2. Test: http://localhost:5000/")
    print("3. Test certificate: http://localhost:5000/cert/MD-12345678")
    print("4. Deploy to Vercel when ready")


if __name__ == "__main__":
    setup_supabase()
