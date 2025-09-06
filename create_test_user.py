#!/usr/bin/env python3
"""
Create test user saraspr1899@gmail.com in the database
"""

import sys
import os
sys.path.append('zimmer-backend')

from sqlalchemy.orm import Session
from zimmer_backend.models.user import User
from zimmer_backend.database import SessionLocal
from zimmer_backend.utils.security import hash_password

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "saraspr1899@gmail.com").first()
        if existing_user:
            print("✅ User saraspr1899@gmail.com already exists")
            print(f"   ID: {existing_user.id}")
            print(f"   Name: {existing_user.name}")
            print(f"   Role: {existing_user.role}")
            return
        
        # Create the user
        user = User(
            name="Sara Test User",
            email="saraspr1899@gmail.com",
            phone_number="+1234567890",
            password_hash=hash_password("password123"),
            role="support_staff",
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✅ User saraspr1899@gmail.com created successfully")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
