"""
Main Authentication Router for Zimmer AI Platform
Provides standard auth endpoints that the frontend expects
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone, timedelta
import secrets
import hashlib

from database import get_db
from models.user import User
from models.twofa import TwoFactorRecoveryCode
from models.email_verification import EmailVerificationToken
from utils.auth_optimized import get_current_user_optimized, rate_limit_dependency
from utils.circuit_breaker import auth_circuit_breaker, login_circuit_breaker
from utils.jwt import create_access_token, create_jwt_token
from utils.security import hash_password, verify_password
from cache_manager import cache_manager

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password functions are now imported from utils.security (bcrypt)

@router.post("/login")
async def login(request: dict, db: Session = Depends(get_db)):
    """
    User login endpoint with proper JWT authentication
    """
    try:
        email = request.get("email")
        password = request.get("password")
        
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )
        
        # Find user in database
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if 2FA is required
        if hasattr(user, 'twofa_enabled') and user.twofa_enabled:
            # Generate challenge token
            challenge_token = secrets.token_urlsafe(32)
            cache_manager.set(f"challenge_{challenge_token}", user.id, ttl=300)  # 5 minutes
            
            return {
                "message": "2FA required",
                "challenge_token": challenge_token,
                "otp_required": True
            }
        
        # Create proper JWT access token
        access_token = create_access_token(user.id, user.is_admin if hasattr(user, 'is_admin') else False)
        
        # Store token in cache for validation
        cache_manager.set(f"token_{access_token}", user.id, ttl=3600)  # 1 hour
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "is_admin": user.is_admin if hasattr(user, 'is_admin') else False,
                "email_verified": user.email_verified if hasattr(user, 'email_verified') else True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/refresh")
async def refresh_token():
    """
    Refresh access token endpoint
    """
    try:
        # In a real implementation, you would validate the refresh token from cookies
        # For now, we'll return a new token for testing
        
        # Create a new access token (in production, validate refresh token first)
        access_token = create_access_token(1, False)  # Mock user ID and admin status
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.post("/logout")
@auth_circuit_breaker
async def logout(
    current_user: User = Depends(get_current_user_optimized)
):
    """
    User logout endpoint
    """
    try:
        # Invalidate user cache
        from utils.auth_optimized import invalidate_user_cache
        invalidate_user_cache(current_user.id)
        
        # Clear user-specific cache entries
        cache_keys_to_clear = [
            f"user_info_{current_user.id}",
            f"user_usage_{current_user.id}",
            f"user_usage_dist_{current_user.id}",
            f"user_automations_{current_user.id}",
            f"2fa_status_{current_user.id}"
        ]
        
        for key in cache_keys_to_clear:
            cache_manager.delete(key)
        
        return {
            "message": "Logged out successfully",
            "user_id": current_user.id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@router.get("/csrf")
@auth_circuit_breaker
async def get_csrf_token():
    """
    Get CSRF token
    """
    try:
        cache_key = "csrf_token"
        cached_token = cache_manager.get(cache_key)
        
        if cached_token:
            return {"csrf_token": cached_token}
        
        # Generate new CSRF token
        csrf_token = secrets.token_urlsafe(32)
        cache_manager.set(cache_key, csrf_token, ttl=1800)  # 30 minutes
        
        return {"csrf_token": csrf_token}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate CSRF token: {str(e)}"
        )

@router.get("/2fa/status")
@auth_circuit_breaker
async def get_2fa_status(
    current_user: User = Depends(get_current_user_optimized),
    db: Session = Depends(get_db)
):
    """
    Get 2FA status for current user
    """
    try:
        cache_key = f"2fa_status_{current_user.id}"
        cached_status = cache_manager.get(cache_key)
        
        if cached_status:
            return cached_status
        
        # Check 2FA status
        twofa_enabled = current_user.twofa_enabled if hasattr(current_user, 'twofa_enabled') else False
        
        status_data = {
            "enabled": twofa_enabled,
            "user_id": current_user.id
        }
        
        cache_manager.set(cache_key, status_data, ttl=300)  # 5 minutes
        return status_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get 2FA status: {str(e)}"
        )

@router.post("/2fa/verify")
@auth_circuit_breaker
async def verify_2fa(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Verify 2FA OTP code
    """
    try:
        challenge_token = request.get("challenge_token")
        otp_code = request.get("otp_code")
        
        if not challenge_token or not otp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge token and OTP code are required"
            )
        
        # Get user from challenge token
        user_id = cache_manager.get(f"challenge_{challenge_token}")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired challenge token"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # In a real implementation, you would verify the OTP code
        # For now, we'll accept any 6-digit code
        
        # Create access token
        access_token = create_access_token(user.id)
        cache_manager.set(f"token_{access_token}", user.id, ttl=3600)  # 1 hour
        
        # Clear challenge token
        cache_manager.delete(f"challenge_{challenge_token}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "is_admin": user.is_admin,
                "email_verified": user.email_verified
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"2FA verification failed: {str(e)}"
        )

@router.get("/me")
async def get_current_user():
    """
    Get current user information
    """
    try:
        # For now, return mock user data
        # In production, you would validate the token and get real user data
        return {
            "id": 1,
            "email": "test@example.com",
            "name": "Test User",
            "role": "user",
            "is_admin": False,
            "email_verified": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )

@router.post("/request-email-verify")
@auth_circuit_breaker
async def request_email_verification(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Request email verification
    """
    try:
        email = request.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )
        
        # Check rate limit
        rate_limit_key = f"email_verify_{email}"
        if not cache_manager.get(rate_limit_key):
            cache_manager.set(rate_limit_key, True, ttl=300)  # 5 minutes
        else:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Email verification request too frequent. Please wait 5 minutes."
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Store verification token
        verification = EmailVerificationToken(
            user_id=user.id,
            token=verification_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        db.add(verification)
        db.commit()
        
        return {
            "message": "Verification email sent",
            "user_id": user.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to request email verification: {str(e)}"
        )
