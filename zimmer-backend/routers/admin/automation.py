from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import httpx
import os
from database import SessionLocal
from models.automation import Automation
from models.user_automation import UserAutomation
from models.user import User
from schemas.automation import ProvisionRequest, ProvisionResponse
from utils.auth_dependency import get_current_user, get_db
from utils.service_tokens import verify_token
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/automations/{automation_id}/provision", response_model=ProvisionResponse)
async def provision_automation(
    automation_id: int = Path(...),
    provision_data: ProvisionRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Provision a user automation with the external automation service
    """
    # Fetch automation
    automation = db.query(Automation).filter(Automation.id == automation_id).first()
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    
    # Verify user automation belongs to current user
    user_automation = db.query(UserAutomation).filter(
        UserAutomation.id == provision_data.user_automation_id,
        UserAutomation.user_id == current_user.id,
        UserAutomation.automation_id == automation_id
    ).first()
    
    if not user_automation:
        raise HTTPException(status_code=404, detail="User automation not found")
    
    # Check if automation has provision URL
    if not automation.api_provision_url:
        raise HTTPException(
            status_code=400, 
            detail="این اتوماسیون قابلیت اتصال مستقیم ندارد"
        )
    
    # Get service token from environment (for MVP)
    # TODO: Replace with secure secret manager in production
    service_token = os.getenv(f"AUTOMATION_{automation_id}_SERVICE_TOKEN")
    if not service_token:
        logger.error(f"No service token found for automation {automation_id}")
        raise HTTPException(
            status_code=500,
            detail="خطا در پیکربندی سرویس"
        )
    
    # Verify service token hash
    if not verify_token(service_token, automation.service_token_hash):
        logger.error(f"Invalid service token for automation {automation_id}")
        raise HTTPException(
            status_code=500,
            detail="خطا در احراز هویت سرویس"
        )
    
    # Prepare request to external automation
    provision_payload = {
        "user_automation_id": user_automation.id,
        "user_id": current_user.id,
        "bot_token": provision_data.bot_token,
        "demo_tokens": user_automation.demo_tokens
    }
    
    headers = {
        "X-Zimmer-Service-Token": service_token,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                automation.api_provision_url,
                json=provision_payload,
                headers=headers
            )
            
            if response.status_code == 200:
                # Update user automation with provision info
                user_automation.provisioned_at = datetime.utcnow()
                user_automation.integration_status = "active"
                
                # Save any returned fields from external service
                response_data = response.json()
                if "webhook_url" in response_data:
                    # Store webhook URL if provided
                    pass  # Add field to UserAutomation if needed
                
                db.commit()
                
                return ProvisionResponse(
                    success=True,
                    message="اتصال با سرویس اتوماسیون برقرار شد ✅",
                    provisioned_at=user_automation.provisioned_at,
                    integration_status=user_automation.integration_status
                )
            else:
                logger.error(f"External automation returned {response.status_code}: {response.text}")
                raise HTTPException(
                    status_code=502,
                    detail="اتصال با سرویس اتوماسیون برقرار نشد. لطفاً بعداً دوباره تلاش کنید."
                )
                
    except httpx.RequestError as e:
        logger.error(f"Network error calling external automation: {e}")
        raise HTTPException(
            status_code=502,
            detail="اتصال با سرویس اتوماسیون برقرار نشد. لطفاً بعداً دوباره تلاش کنید."
        )
    except Exception as e:
        logger.error(f"Unexpected error during provision: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطای غیرمنتظره در اتصال به سرویس"
        )