#!/usr/bin/env python3
"""
Create a test user for comprehensive testing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'zimmer-backend'))

from database import get_db, SessionLocal
from models import User
from utils.security import hash_password

def create_test_user():
    """Create a test user for testing purposes"""
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@zimmer.ai").first()
        if existing_user:
            print("✅ Test user already exists")
            return existing_user
        
        # Create new test user
        from models.user import UserRole
        test_user = User(
            email="test@zimmer.ai",
            name="Test User",
            password_hash=hash_password("test123"),
            role=UserRole.support_staff,
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully")
        print(f"   Email: test@zimmer.ai")
        print(f"   Password: test123")
        print(f"   User ID: {test_user.id}")
        
        return test_user
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
