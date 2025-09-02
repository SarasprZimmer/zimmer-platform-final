from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.user import User, UserRole
from schemas.user import UserCreateRequest, UserUpdateRoleRequest, UserListResponse
from utils.auth_dependency import get_current_manager_user, get_db
from utils.security import hash_password
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users", response_model=List[UserListResponse])
async def list_users(
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager_user)
):
    """
    List all users (manager only)
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users

@router.post("/users", response_model=UserListResponse)
async def create_user(
    user_data: UserCreateRequest,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager_user)
):
    """
    Create a new user (manager only)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password_hash=hashed_password,
        role=user_data.role,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"Manager {current_manager.email} created user {new_user.email} with role {new_user.role}")
    
    return new_user

@router.put("/users/{user_id}/role", response_model=UserListResponse)
async def update_user_role(
    user_id: int = Path(...),
    role_data: UserUpdateRoleRequest = None,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager_user)
):
    """
    Update user role (manager only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent manager from changing their own role
    if user.id == current_manager.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    # Prevent manager from creating another manager (only existing managers can)
    if role_data.role == UserRole.manager and current_manager.role != UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can create other managers"
        )
    
    user.role = role_data.role
    if role_data.is_active is not None:
        user.is_active = role_data.is_active
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"Manager {current_manager.email} updated user {user.email} role to {user.role}")
    
    return user

@router.delete("/users/{user_id}")
async def deactivate_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager_user)
):
    """
    Deactivate user (manager only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent manager from deactivating themselves
    if user.id == current_manager.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Prevent manager from deactivating other managers
    if user.role == UserRole.manager and current_manager.role != UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot deactivate manager accounts"
        )
    
    user.is_active = False
    db.commit()
    
    logger.info(f"Manager {current_manager.email} deactivated user {user.email}")
    
    return {"message": "User deactivated successfully"}

@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager_user)
):
    """
    Activate user (manager only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    
    logger.info(f"Manager {current_manager.email} activated user {user.email}")
    
    return {"message": "User activated successfully"}
