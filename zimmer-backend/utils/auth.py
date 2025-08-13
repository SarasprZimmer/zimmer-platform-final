from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from database import SessionLocal
from models.user import User
from utils.jwt import verify_jwt_token, get_current_user_id

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token (development mode defaults to admin user)
    """
    try:
        # Development mode: if no credentials, use admin user (ID 1)
        if credentials is None:
            user = db.query(User).filter(User.id == 1).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No default admin user found"
                )
            return user
        
        # Production mode: parse JWT token
        token = credentials.credentials
        
        # Verify JWT token
        try:
            user_id = get_current_user_id(token)
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require admin privileges
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user 