from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from database import SessionLocal
from models.user import User
from models.payment import Payment
from models.token_usage import TokenUsage
from models.user_automation import UserAutomation
from models.automation import Automation
from models.ticket import Ticket
from schemas.admin import UserListResponse, PaymentListResponse, UserTokenUsageResponse, UserAutomationAdminResponse
from utils.auth_dependency import get_current_admin_user, get_db

router = APIRouter()

@router.get("/users", response_model=UserListResponse)
async def get_users(
    is_admin: Optional[bool] = Query(None, description="Filter by admin status"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get list of all users/clients (admin only)
    """
    try:
        # Build base query
        query = db.query(User)
        
        # Apply filters if provided
        if is_admin is not None:
            query = query.filter(User.is_admin == is_admin)
        
        # Get total count
        total_count = query.count()
        
        # Get users ordered by newest first
        users = query.order_by(User.created_at.desc()).all()
        
        # Format response (exclude password_hash for security)
        formatted_users = []
        for user in users:
            formatted_users.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "is_admin": user.is_admin,
                "created_at": user.created_at
            })
        
        return UserListResponse(
            total_count=total_count,
            users=formatted_users
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )

@router.get("/payments", response_model=PaymentListResponse)
async def get_payments(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: Optional[str] = Query(None, description="Filter by payment status"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get payment history (admin only)
    """
    try:
        # Build base query with user join
        query = db.query(
            Payment,
            User.name.label('user_name')
        ).join(
            User, Payment.user_id == User.id
        )
        
        # Apply filters if provided
        if user_id is not None:
            query = query.filter(Payment.user_id == user_id)
        
        if status is not None:
            query = query.filter(Payment.status == status)
        
        # Get total count
        total_count = query.count()
        
        # Get payments ordered by newest first
        payment_records = query.order_by(Payment.created_at.desc()).all()
        
        # Format response
        formatted_payments = []
        for payment, user_name in payment_records:
            formatted_payments.append(PaymentResponse(
                id=payment.id,
                user_id=payment.user_id,
                user_name=user_name,
                amount=payment.amount,
                tokens_purchased=payment.tokens_purchased,
                method=payment.method,
                transaction_id=payment.transaction_id,
                status=payment.status,
                created_at=payment.created_at
            ))
        
        return PaymentListResponse(
            total_count=total_count,
            payments=formatted_payments
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve payments: {str(e)}"
        )

@router.get("/usage/{user_id}", response_model=UserTokenUsageResponse)
async def get_user_token_usage(
    user_id: int = Path(..., description="User ID to get token usage for"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get token usage for a specific user (admin only)
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Build query to get token usage with automation names
        query = db.query(
            TokenUsage,
            Automation.name.label('automation_name')
        ).join(
            UserAutomation, TokenUsage.user_automation_id == UserAutomation.id
        ).join(
            Automation, UserAutomation.automation_id == Automation.id
        ).filter(
            UserAutomation.user_id == user_id
        )
        
        # Get usage records ordered by newest first
        usage_records = query.order_by(TokenUsage.created_at.desc()).all()
        
        # Calculate totals
        total_tokens_used = sum(record.tokens_used for record, _ in usage_records)
        
        # Estimate cost (assuming $0.002 per 1K tokens - adjust as needed)
        total_cost = (total_tokens_used / 1000) * 0.002
        
        # Format usage entries
        usage_entries = []
        for usage, automation_name in usage_records:
            usage_entries.append(TokenUsageResponse(
                id=usage.id,
                user_automation_id=usage.user_automation_id,
                automation_name=automation_name,
                tokens_used=usage.tokens_used,
                usage_type=usage.usage_type,
                description=usage.description,
                created_at=usage.created_at
            ))
        
        return UserTokenUsageResponse(
            user_id=user_id,
            user_name=user.name,
            total_tokens_used=total_tokens_used,
            total_cost=total_cost,
            usage_entries=usage_entries
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user token usage: {str(e)}"
        )

@router.get("/user-automations", response_model=List[UserAutomationAdminResponse])
async def get_user_automations_admin(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    demo_only: Optional[bool] = Query(None, description="Show only demo users"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all user automations with demo token information (admin only)
    """
    try:
        # Build base query with joins
        query = db.query(
            UserAutomation,
            User.name.label('user_name'),
            Automation.name.label('automation_name')
        ).join(
            User, UserAutomation.user_id == User.id
        ).join(
            Automation, UserAutomation.automation_id == Automation.id
        )
        
        # Apply filters
        if user_id is not None:
            query = query.filter(UserAutomation.user_id == user_id)
        
        if demo_only:
            query = query.filter(UserAutomation.is_demo_active == True)
        
        # Get records ordered by newest first
        records = query.order_by(UserAutomation.created_at.desc()).all()
        
        # Format response
        formatted_automations = []
        for ua, user_name, automation_name in records:
            formatted_automations.append({
                "id": ua.id,
                "user_id": ua.user_id,
                "user_name": user_name,
                "automation_id": ua.automation_id,
                "automation_name": automation_name,
                "tokens_remaining": ua.tokens_remaining or 0,
                "demo_tokens": ua.demo_tokens,
                "is_demo_active": ua.is_demo_active,
                "demo_expired": ua.demo_expired,
                "status": ua.status,
                "created_at": ua.created_at
            })
        
        return formatted_automations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user automations: {str(e)}"
        )

@router.get("/tickets")
async def get_tickets(
    status: Optional[str] = Query(None, description="Filter by ticket status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all support tickets (admin only)
    """
    try:
        # Build base query with user join
        query = db.query(
            Ticket,
            User.name.label('user_name')
        ).join(
            User, Ticket.user_id == User.id
        )
        
        # Apply filters if provided
        if status is not None:
            query = query.filter(Ticket.status == status)
        
        if priority is not None:
            query = query.filter(Ticket.priority == priority)
        
        # Get total count
        total_count = query.count()
        
        # Get tickets ordered by newest first
        ticket_records = query.order_by(Ticket.created_at.desc()).all()
        
        # Format response
        formatted_tickets = []
        for ticket, user_name in ticket_records:
            formatted_tickets.append({
                "id": ticket.id,
                "user_id": ticket.user_id,
                "user_name": user_name,
                "subject": ticket.subject,
                "status": ticket.status,
                "priority": ticket.priority,
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at
            })
        
        return {
            "total_count": total_count,
            "tickets": formatted_tickets
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tickets: {str(e)}"
        )

@router.get("/automations")
async def get_automations(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all available automations (admin only)
    """
    try:
        # Get all automations with only the columns we need
        automations = db.query(
            Automation.id,
            Automation.name,
            Automation.description,
            Automation.status,
            Automation.created_at
        ).order_by(Automation.name).all()
        
        # Format response
        formatted_automations = []
        for automation in automations:
            formatted_automations.append({
                "id": automation.id,
                "name": automation.name,
                "description": automation.description,
                "is_active": automation.status,
                "created_at": automation.created_at
            })
        
        return {
            "total_count": len(formatted_automations),
            "automations": formatted_automations
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve automations: {str(e)}"
        ) 