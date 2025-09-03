from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, timedelta
from database import SessionLocal
from models.user import User
from models.payment import Payment
from models.token_usage import TokenUsage
from models.user_automation import UserAutomation
from models.automation import Automation
from models.ticket import Ticket
from models.kb_status_history import KBStatusHistory
from models.kb_template import KBTemplate
from schemas.admin import UserListResponse, PaymentListResponse, UserTokenUsageResponse, UserAutomationAdminResponse, PaymentResponse, UsageStatsResponse
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

@router.get("/usage/stats", response_model=UsageStatsResponse)
async def get_usage_stats(
    type: Optional[str] = Query(None, description="Type of usage: 'tokens', 'kb', 'general'"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get usage statistics (admin only)
    """
    try:
        # Simplified version without date filtering for now
        
        if type == "tokens":
            # Get token usage statistics
            try:
                # Check if table has any records first
                total_requests = db.query(TokenUsage).count()
                
                if total_requests == 0:
                    return UsageStatsResponse(
                        type="token_usage",
                        total_tokens_used=0,
                        total_requests=0,
                        average_tokens_per_request=0,
                        estimated_cost_usd=0,
                        message="No token usage data available"
                    )
                
                # Only query if we have data
                query = db.query(
                    func.sum(TokenUsage.tokens_used).label('total_tokens'),
                    func.avg(TokenUsage.tokens_used).label('avg_tokens_per_request')
                )
                
                result = query.first()
                
                return UsageStatsResponse(
                    type="token_usage",
                    total_tokens_used=result.total_tokens or 0,
                    total_requests=total_requests,
                    average_tokens_per_request=round(result.avg_tokens_per_request or 0, 2),
                    estimated_cost_usd=round((result.total_tokens or 0) / 1000 * 0.002, 4)
                )
            except Exception as e:
                # Return safe defaults if there's an error
                return UsageStatsResponse(
                    type="token_usage",
                    total_tokens_used=0,
                    total_requests=0,
                    average_tokens_per_request=0,
                    estimated_cost_usd=0,
                    error="Could not retrieve token usage data"
                )
        
        elif type == "kb":
            # Get KB usage statistics
            query = db.query(
                func.count(KBTemplate.id).label('total_entries'),
                func.count(func.distinct(KBTemplate.automation_id)).label('unique_automations')
            )
            
            result = query.first()
            
            return UsageStatsResponse(
                type="knowledge_base",
                total_entries=result.total_entries or 0,
                unique_automations=result.unique_automations or 0
            )
        
        else:
            # General usage overview
            try:
                # Token usage - handle empty table
                token_count = db.query(TokenUsage).count()
                if token_count > 0:
                    total_tokens = db.query(func.sum(TokenUsage.tokens_used)).scalar() or 0
                else:
                    total_tokens = 0
                
                # User count (simple count)
                total_users = db.query(func.count(User.id)).scalar() or 0
                
                # Automation count (simple count)
                automation_count = db.query(UserAutomation).count()
                if automation_count > 0:
                    active_automations = db.query(func.count(func.distinct(UserAutomation.automation_id))).scalar() or 0
                else:
                    active_automations = 0
                
                return UsageStatsResponse(
                    type="general_overview",
                    total_tokens_used=total_tokens,
                    total_users=total_users,
                    active_automations=active_automations,
                    estimated_cost_usd=round(total_tokens / 1000 * 0.002, 4),
                    period={
                        "from_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                        "to_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
            except Exception as e:
                # Return safe defaults if there's an error
                return UsageStatsResponse(
                    type="general_overview",
                    total_tokens_used=0,
                    total_users=0,
                    active_automations=0,
                    estimated_cost_usd=0,
                    error="Could not retrieve usage data",
                    period={
                        "from_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                        "to_date": datetime.now().strftime("%Y-%m-%d")
                    }
                )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage statistics: {str(e)}"
        )

@router.get("/kb-monitoring")
async def get_kb_monitoring(
    automation_id: Optional[int] = Query(None, description="Filter by automation ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    health_status: Optional[str] = Query(None, description="Filter by health status"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get KB monitoring status (admin only)
    """
    try:
        # Check if KBStatusHistory table has any records first
        total_records = db.query(KBStatusHistory).count()
        
        if total_records == 0:
            return {
                "total_records": 0,
                "health_summary": {},
                "statuses": [],
                "message": "No KB monitoring data available"
            }
        
        # Build base query with joins
        query = db.query(
            KBStatusHistory,
            User.name.label('user_name'),
            Automation.name.label('automation_name')
        ).join(
            User, KBStatusHistory.user_id == User.id
        ).join(
            Automation, KBStatusHistory.automation_id == Automation.id
        )
        
        # Apply filters
        if automation_id:
            query = query.filter(KBStatusHistory.automation_id == automation_id)
        
        if user_id:
            query = query.filter(KBStatusHistory.user_id == user_id)
        
        if health_status:
            query = query.filter(KBStatusHistory.kb_health == health_status)
        
        # Get latest status for each user-automation combination
        latest_statuses = []
        seen_combinations = set()
        
        # Order by timestamp (newest first) and get unique combinations
        results = query.order_by(KBStatusHistory.timestamp.desc()).all()
        
        for kb_status, user_name, automation_name in results:
            combination = (kb_status.user_id, kb_status.automation_id)
            if combination not in seen_combinations:
                seen_combinations.add(combination)
                latest_statuses.append({
                    "id": kb_status.id,
                    "user_id": kb_status.user_id,
                    "user_name": user_name,
                    "automation_id": kb_status.automation_id,
                    "automation_name": automation_name,
                    "kb_health": kb_status.kb_health,
                    "backup_status": kb_status.backup_status,
                    "error_logs": kb_status.error_logs,
                    "timestamp": kb_status.timestamp
                })
        
        # Calculate summary statistics
        health_counts = {}
        for status in latest_statuses:
            health = status["kb_health"]
            health_counts[health] = health_counts.get(health, 0) + 1
        
        return {
            "total_records": len(latest_statuses),
            "health_summary": health_counts,
            "statuses": latest_statuses
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve KB monitoring data: {str(e)}"
        ) 