from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from database import SessionLocal
from models.user import User
from models.payment import Payment
from models.token_usage import TokenUsage
from models.user_automation import UserAutomation
from models.automation import Automation
from schemas.user import UserSignupRequest, UserSignupResponse, UserLoginRequest, UserLoginResponse, UserResponse, UserUpdateRequest, UserDashboardResponse, UserAutomationCreate, UserAutomationUpdate, UserAutomationResponse
from schemas.admin import TokenUsageResponse, PaymentResponse
from utils.security import hash_password, verify_password
from utils.jwt import create_jwt_token
from utils.auth_dependency import get_current_user

router = APIRouter()

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup endpoint removed - only managers can create users via /api/admin/users

@router.post("/login", response_model=UserLoginResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    """
    try:
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated. Please contact your manager."
            )
        
        # Create JWT token with user information
        token = create_jwt_token(user.id, user.name, user.email, user.role.value)
        
        return UserLoginResponse(
            message="Login successful",
            access_token=token,
            user_id=user.id,
            email=user.email,
            name=user.name,
            role=user.role
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/logout")
async def logout_user():
    """
    Logout user (client-side token removal)
    """
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's basic information
    """
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user info: {str(e)}"
        )

@router.put("/user/profile", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information
    """
    try:
        # Update user fields if provided
        if user_data.name is not None:
            current_user.name = user_data.name
        if user_data.phone_number is not None:
            current_user.phone_number = user_data.phone_number
        
        db.commit()
        db.refresh(current_user)
        
        return current_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user profile: {str(e)}"
        )

@router.post("/user/change-password")
async def change_password(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    try:
        current_password = request.get("current_password")
        new_password = request.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور فعلی و جدید الزامی است"
            )
        
        # Verify current password
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور فعلی اشتباه است"
            )
        
        # Hash new password
        current_user.password_hash = hash_password(new_password)
        db.commit()
        
        return {"message": "رمز عبور با موفقیت تغییر یافت"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطا در تغییر رمز عبور"
        )

@router.post("/user/password")
async def change_user_password(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password (alternative endpoint)"""
    try:
        new_password = request.get("new_password")
        confirm_password = request.get("confirm_password")
        
        if not new_password or not confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور جدید و تکرار آن الزامی است"
            )
        
        if new_password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور و تکرار آن یکسان نیست"
            )
        
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور باید حداقل 8 کاراکتر باشد"
            )
        
        # Hash new password
        current_user.password_hash = hash_password(new_password)
        db.commit()
        
        return {"message": "رمز عبور با موفقیت تغییر یافت"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطا در تغییر رمز عبور"
        )

@router.get("/user/usage")
async def get_user_token_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's token usage statistics
    """
    try:
        # Get user's automations
        user_automations = db.query(UserAutomation).filter(
            UserAutomation.user_id == current_user.id
        ).all()
        
        # Calculate usage statistics
        total_tokens_used = 0
        total_tokens_remaining = 0
        total_demo_tokens = 0
        
        for ua in user_automations:
            total_tokens_remaining += ua.tokens_remaining or 0
            total_demo_tokens += ua.demo_tokens or 0
        
        # Get recent token usage records
        recent_usage = db.query(TokenUsage).join(
            UserAutomation, TokenUsage.user_automation_id == UserAutomation.id
        ).filter(
            UserAutomation.user_id == current_user.id
        ).order_by(TokenUsage.created_at.desc()).limit(10).all()
        
        # Format usage records
        usage_records = []
        for usage in recent_usage:
            usage_records.append({
                "id": usage.id,
                "tokens_used": usage.tokens_used,
                "usage_type": usage.usage_type,
                "description": usage.description,
                "created_at": usage.created_at
            })
        
        return {
            "total_tokens_remaining": total_tokens_remaining,
            "total_demo_tokens": total_demo_tokens,
            "recent_usage": usage_records
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve token usage: {str(e)}"
        )

@router.post("/user/automations", response_model=UserAutomationResponse)
async def create_user_automation(
    automation_data: UserAutomationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user automation with bot token uniqueness check
    """
    try:
        # Check if automation exists
        automation = db.query(Automation).filter(Automation.id == automation_data.automation_id).first()
        if not automation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automation not found"
            )
        
        # Check if user already has this automation
        existing_automation = db.query(UserAutomation).filter(
            UserAutomation.user_id == current_user.id,
            UserAutomation.automation_id == automation_data.automation_id
        ).first()
        
        if existing_automation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has this automation"
            )
        
        # Check bot token uniqueness if provided
        if automation_data.telegram_bot_token:
            existing_bot = db.query(UserAutomation).filter(
                UserAutomation.telegram_bot_token == automation_data.telegram_bot_token
            ).first()
            
            if existing_bot:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="این توکن ربات قبلاً ثبت شده است. لطفاً یک توکن دیگر وارد کنید."
                )
        
        # Create new user automation
        new_user_automation = UserAutomation(
            user_id=current_user.id,
            automation_id=automation_data.automation_id,
            telegram_bot_token=automation_data.telegram_bot_token,
            tokens_remaining=automation_data.tokens_remaining or 0,
            demo_tokens=5,  # Default demo tokens
            is_demo_active=True,
            demo_expired=False,
            status="active"
        )
        
        db.add(new_user_automation)
        db.commit()
        db.refresh(new_user_automation)
        
        # Return response with automation name
        return UserAutomationResponse(
            id=new_user_automation.id,
            automation_id=new_user_automation.automation_id,
            automation_name=automation.name,
            tokens_remaining=new_user_automation.tokens_remaining,
            demo_tokens=new_user_automation.demo_tokens,
            is_demo_active=new_user_automation.is_demo_active,
            demo_expired=new_user_automation.demo_expired,
            status=new_user_automation.status,
            created_at=new_user_automation.created_at
        )
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        if "uq_telegram_bot_token" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این توکن ربات قبلاً ثبت شده است. لطفاً یک توکن دیگر وارد کنید."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user automation: {str(e)}"
        )

@router.put("/user/automations/{automation_id}", response_model=UserAutomationResponse)
async def update_user_automation(
    automation_id: int = Path(..., description="User automation ID to update"),
    automation_data: UserAutomationUpdate = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a user automation with bot token uniqueness check
    """
    try:
        # Get user automation
        user_automation = db.query(UserAutomation).filter(
            UserAutomation.id == automation_id,
            UserAutomation.user_id == current_user.id
        ).first()
        
        if not user_automation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User automation not found"
            )
        
        # Check bot token uniqueness if updating
        if automation_data and automation_data.telegram_bot_token:
            existing_bot = db.query(UserAutomation).filter(
                UserAutomation.telegram_bot_token == automation_data.telegram_bot_token,
                UserAutomation.id != automation_id
            ).first()
            
            if existing_bot:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="این توکن ربات قبلاً ثبت شده است. لطفاً یک توکن دیگر وارد کنید."
                )
        
        # Update fields if provided
        if automation_data:
            if automation_data.telegram_bot_token is not None:
                user_automation.telegram_bot_token = automation_data.telegram_bot_token
            if automation_data.tokens_remaining is not None:
                user_automation.tokens_remaining = automation_data.tokens_remaining
            if automation_data.status is not None:
                user_automation.status = automation_data.status
        
        db.commit()
        db.refresh(user_automation)
        
        # Get automation name for response
        automation = db.query(Automation).filter(Automation.id == user_automation.automation_id).first()
        automation_name = automation.name if automation else "Unknown"
        
        return UserAutomationResponse(
            id=user_automation.id,
            automation_id=user_automation.automation_id,
            automation_name=automation_name,
            tokens_remaining=user_automation.tokens_remaining,
            demo_tokens=user_automation.demo_tokens,
            is_demo_active=user_automation.is_demo_active,
            demo_expired=user_automation.demo_expired,
            status=user_automation.status,
            created_at=user_automation.created_at
        )
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        if "uq_telegram_bot_token" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این توکن ربات قبلاً ثبت شده است. لطفاً یک توکن دیگر وارد کنید."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user automation: {str(e)}"
        )

@router.get("/user/automations")
async def get_user_automations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's purchased automations
    """
    try:
        # Get user's automations with automation details
        query = db.query(
            UserAutomation,
            Automation.name,
            Automation.description,
            Automation.pricing_type,
            Automation.price_per_token,
            Automation.status
        ).join(
            Automation, UserAutomation.automation_id == Automation.id
        ).filter(
            UserAutomation.user_id == current_user.id
        )
        
        user_automations = query.all()
        
        # Format response
        automations = []
        for ua, name, description, pricing_type, price_per_token, status in user_automations:
            automations.append({
                "id": ua.id,
                "automation_id": ua.automation_id,
                "name": name,
                "description": description,
                "pricing_type": pricing_type,
                "price_per_token": price_per_token,
                "status": ua.status,
                "tokens_remaining": ua.tokens_remaining,
                "demo_tokens": ua.demo_tokens,
                "is_demo_active": ua.is_demo_active,
                "demo_expired": ua.demo_expired,
                "created_at": ua.created_at
            })
        
        return automations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user automations: {str(e)}"
        )

@router.get("/user/dashboard", response_model=UserDashboardResponse)
async def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive user dashboard data including demo token status
    """
    try:
        # Get user's automations with automation details
        query = db.query(
            UserAutomation,
            Automation.name,
            Automation.description,
            Automation.pricing_type,
            Automation.price_per_token,
            Automation.status
        ).join(
            Automation, UserAutomation.automation_id == Automation.id
        ).filter(
            UserAutomation.user_id == current_user.id
        )
        
        user_automations = query.all()
        
        # Calculate totals
        total_demo_tokens = sum(ua.demo_tokens for ua, _, _, _, _, _ in user_automations)
        total_paid_tokens = sum(ua.tokens_remaining or 0 for ua, _, _, _, _, _ in user_automations)
        has_active_demo = any(ua.is_demo_active for ua, _, _, _, _, _ in user_automations)
        has_expired_demo = any(ua.demo_expired for ua, _, _, _, _, _ in user_automations)
        
        # Format automations
        automations = []
        for ua, name, description, pricing_type, price_per_token, status in user_automations:
            automations.append({
                "id": ua.id,
                "automation_id": ua.automation_id,
                "automation_name": name,
                "tokens_remaining": ua.tokens_remaining or 0,
                "demo_tokens": ua.demo_tokens,
                "is_demo_active": ua.is_demo_active,
                "demo_expired": ua.demo_expired,
                "status": ua.status,
                "created_at": ua.created_at
            })
        
        return UserDashboardResponse(
            user=current_user,
            automations=automations,
            total_demo_tokens=total_demo_tokens,
            total_paid_tokens=total_paid_tokens,
            has_active_demo=has_active_demo,
            has_expired_demo=has_expired_demo
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user dashboard: {str(e)}"
        )

@router.get("/automations/available")
async def get_available_automations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get automations available for purchase
    """
    try:
        # Get all active, healthy, and listed automations
        automations = db.query(Automation).filter(
            Automation.status == True,
            Automation.is_listed == True,
            Automation.health_status == "healthy"
        ).order_by(Automation.created_at.desc()).all()
        
        # Format response
        available_automations = []
        for automation in automations:
            available_automations.append({
                "id": automation.id,
                "name": automation.name,
                "description": automation.description,
                "pricing_type": automation.pricing_type,
                "price_per_token": automation.price_per_token,
                "created_at": automation.created_at
            })
        
        return available_automations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve available automations: {str(e)}"
        )

@router.get("/user/automations/{automation_id}")
async def check_automation_access(
    automation_id: int = Path(..., description="Automation ID to check access for"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if user has access to a specific automation
    """
    try:
        # Check if user has this automation
        user_automation = db.query(UserAutomation).filter(
            UserAutomation.user_id == current_user.id,
            UserAutomation.automation_id == automation_id
        ).first()
        
        if not user_automation:
            return {
                "has_access": False,
                "message": "User does not have access to this automation"
            }
        
        # Get automation details
        automation = db.query(Automation).filter(Automation.id == automation_id).first()
        if not automation:
            return {
                "has_access": False,
                "message": "Automation not found"
            }
        
        return {
            "has_access": True,
            "automation": {
                "id": automation.id,
                "name": automation.name,
                "description": automation.description,
                "pricing_type": automation.pricing_type,
                "price_per_token": automation.price_per_token
            },
            "user_automation": {
                "id": user_automation.id,
                "tokens_remaining": user_automation.tokens_remaining,
                "demo_tokens": user_automation.demo_tokens,
                "is_demo_active": user_automation.is_demo_active,
                "demo_expired": user_automation.demo_expired,
                "status": user_automation.status
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check automation access: {str(e)}"
        )

@router.get("/user/payments")
async def get_user_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's payment history
    """
    try:
        # Get user's payments with automation details
        payments = db.query(Payment, Automation).join(
            Automation, Payment.automation_id == Automation.id
        ).filter(
            Payment.user_id == current_user.id
        ).order_by(Payment.created_at.desc()).all()
        
        # Format response
        formatted_payments = []
        for payment, automation in payments:
            formatted_payments.append({
                "id": payment.id,
                "amount": payment.amount,
                "tokens_purchased": payment.tokens_purchased,
                "method": payment.method,
                "gateway": payment.gateway or "zarinpal",
                "transaction_id": payment.transaction_id,
                "ref_id": payment.ref_id,
                "status": payment.status,
                "created_at": payment.created_at,
                "automation": {
                    "id": automation.id,
                    "name": automation.name,
                    "price_per_token": automation.price_per_token
                }
            })
        
        return formatted_payments
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve payments: {str(e)}"
        ) 