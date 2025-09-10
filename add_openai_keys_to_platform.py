#!/usr/bin/env python3
"""
Add OpenAI API Keys to the Zimmer Platform

This script demonstrates how to add OpenAI API keys to the platform's
key management system for automations to use.
"""

import requests
import json
import sys
import os

# Add the backend directory to the path so we can import modules
backend_path = os.path.join(os.path.dirname(__file__), 'zimmer-backend')
sys.path.append(backend_path)

# Change to backend directory to ensure correct database path
os.chdir(backend_path)

from database import get_db
from models.openai_key import OpenAIKey, OpenAIKeyStatus
from models.automation import Automation
from utils.crypto import encrypt_secret
from sqlalchemy.orm import Session

def add_openai_keys_to_database():
    """Add OpenAI keys directly to the database"""
    print("🔑 Adding OpenAI API Keys to Platform Database")
    print("=" * 50)
    
    # Get database session
    db = next(get_db())
    
    try:
        # First, let's check if we have any automations
        automations = db.query(Automation).all()
        print(f"Found {len(automations)} automations in the database")
        
        if not automations:
            print("❌ No automations found. Creating a mock automation first...")
            # Create a mock automation
            mock_automation = Automation(
                name="Mock Travel Agency AI",
                description="Mock automation for testing OpenAI key integration",
                pricing_type="per_use",
                health_check_url="http://localhost:8003/health",
                health_status="healthy",
                is_listed=True
            )
            db.add(mock_automation)
            db.commit()
            db.refresh(mock_automation)
            print(f"✅ Created mock automation with ID: {mock_automation.id}")
            automations = [mock_automation]
        
        # Add OpenAI keys for each automation
        mock_keys = [
            {
                "alias": "Primary Key",
                "api_key": "sk-mock-primary-key-1234567890abcdef",
                "rpm_limit": 60,
                "daily_token_limit": 100000
            },
            {
                "alias": "Secondary Key", 
                "api_key": "sk-mock-secondary-key-abcdef1234567890",
                "rpm_limit": 60,
                "daily_token_limit": 100000
            },
            {
                "alias": "Backup Key",
                "api_key": "sk-mock-backup-key-9876543210fedcba",
                "rpm_limit": 30,
                "daily_token_limit": 50000
            }
        ]
        
        for automation in automations:
            print(f"\n📝 Adding keys for automation: {automation.name} (ID: {automation.id})")
            
            for key_data in mock_keys:
                # Check if key already exists
                existing_key = db.query(OpenAIKey).filter(
                    OpenAIKey.automation_id == automation.id,
                    OpenAIKey.alias == key_data["alias"]
                ).first()
                
                if existing_key:
                    print(f"  ⚠️  Key '{key_data['alias']}' already exists, skipping...")
                    continue
                
                # Encrypt the API key
                try:
                    encrypted_key = encrypt_secret(key_data["api_key"])
                except Exception as e:
                    print(f"  ❌ Failed to encrypt key '{key_data['alias']}': {e}")
                    continue
                
                # Create the key
                new_key = OpenAIKey(
                    automation_id=automation.id,
                    alias=key_data["alias"],
                    key_encrypted=encrypted_key,
                    status=OpenAIKeyStatus.ACTIVE,
                    rpm_limit=key_data["rpm_limit"],
                    daily_token_limit=key_data["daily_token_limit"]
                )
                
                db.add(new_key)
                db.commit()
                db.refresh(new_key)
                
                print(f"  ✅ Added key '{key_data['alias']}' with ID: {new_key.id}")
        
        # Verify the keys were added
        print(f"\n📊 Verification:")
        total_keys = db.query(OpenAIKey).count()
        active_keys = db.query(OpenAIKey).filter(OpenAIKey.status == OpenAIKeyStatus.ACTIVE).count()
        print(f"  Total keys in database: {total_keys}")
        print(f"  Active keys: {active_keys}")
        
        # List all keys
        print(f"\n📋 All OpenAI Keys:")
        all_keys = db.query(OpenAIKey).all()
        for key in all_keys:
            automation = db.query(Automation).filter(Automation.id == key.automation_id).first()
            print(f"  ID: {key.id} | Automation: {automation.name if automation else 'Unknown'} | Alias: {key.alias} | Status: {key.status}")
        
        print(f"\n🎉 Successfully added OpenAI keys to the platform!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding keys: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_key_retrieval():
    """Test retrieving keys from the platform"""
    print(f"\n🧪 Testing Key Retrieval")
    print("=" * 30)
    
    db = next(get_db())
    
    try:
        from services.openai_key_manager import OpenAIKeyManager
        key_manager = OpenAIKeyManager(db)
        
        # Get all automations
        automations = db.query(Automation).all()
        
        for automation in automations:
            print(f"\n🔍 Testing key retrieval for automation: {automation.name}")
            
            # Get key pool
            key_pool = key_manager.get_pool(automation.id)
            print(f"  Key pool size: {len(key_pool)}")
            
            # Select best key
            selected_key = key_manager.select_key(automation.id)
            if selected_key:
                print(f"  ✅ Selected key: ID {selected_key.id}, Alias: {selected_key.alias}")
                
                # Test key decryption
                key_data = key_manager.get_key_with_decrypted(selected_key.id)
                if key_data:
                    key, decrypted_key = key_data
                    print(f"  ✅ Key decryption successful: {decrypted_key[:20]}...")
                else:
                    print(f"  ❌ Key decryption failed")
            else:
                print(f"  ❌ No keys available for automation {automation.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing key retrieval: {e}")
        return False
    finally:
        db.close()

def main():
    """Main function"""
    print("🚀 OpenAI Key Management Setup for Zimmer Platform")
    print("=" * 60)
    
    # Add keys to database
    success = add_openai_keys_to_database()
    
    if success:
        # Test key retrieval
        test_key_retrieval()
        
        print(f"\n✅ Setup Complete!")
        print(f"📋 Next Steps:")
        print(f"  1. The platform now has OpenAI keys configured")
        print(f"  2. Automations can request keys using the key manager")
        print(f"  3. Test the enhanced mock automation service again")
        print(f"  4. The GPT generation should now work properly")
    else:
        print(f"\n❌ Setup Failed!")
        print(f"Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
