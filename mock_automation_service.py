#!/usr/bin/env python3
"""
Mock Automation Service for Testing Zimmer Platform Integration

This service demonstrates how to create an automation that integrates with the Zimmer platform.
It implements all required endpoints and follows the platform's integration requirements.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import time
import hashlib
import hmac
import json
from datetime import datetime, timezone

# Initialize FastAPI app
app = FastAPI(
    title="Mock Automation Service",
    description="A mock automation service for testing Zimmer platform integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service configuration
SERVICE_NAME = "Mock Travel Agency AI"
SERVICE_VERSION = "1.0.0"
START_TIME = time.time()

# Mock data storage
user_automations = {}
kb_status = {}
usage_logs = []

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: int
    service: str
    timestamp: str

class ProvisionRequest(BaseModel):
    user_automation_id: int
    user_id: int
    bot_token: Optional[str] = None
    demo_tokens: int = 5

class ProvisionResponse(BaseModel):
    success: bool
    message: str
    provisioned_at: str
    integration_status: str
    service_url: Optional[str] = None

class UsageConsumeRequest(BaseModel):
    user_automation_id: int
    units: int
    usage_type: str
    meta: Optional[Dict[str, Any]] = None

class UsageConsumeResponse(BaseModel):
    accepted: bool
    remaining_demo_tokens: int
    remaining_paid_tokens: int
    message: str

class KBStatusResponse(BaseModel):
    status: str
    last_updated: str
    total_documents: int
    healthy: bool

class KBResetResponse(BaseModel):
    success: bool
    message: str
    reset_at: str

# Authentication dependency
def verify_service_token(x_zimmer_service_token: Optional[str] = Header(None)):
    """Verify the service token from Zimmer platform"""
    if not x_zimmer_service_token:
        raise HTTPException(status_code=401, detail="Missing service token")
    
    # In a real implementation, you would verify the token against the platform
    # For this mock, we'll accept any token that starts with "mock_"
    if not x_zimmer_service_token.startswith("mock_"):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    return x_zimmer_service_token

# Health check endpoint (REQUIRED)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - REQUIRED by Zimmer platform
    
    This endpoint is called by the platform to verify the automation is healthy.
    Must return HTTP 200 with required fields: status, version, uptime
    """
    return HealthResponse(
        status="ok",
        version=SERVICE_VERSION,
        uptime=int(time.time() - START_TIME),
        service=SERVICE_NAME,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

# Provision endpoint (REQUIRED for direct integration)
@app.post("/provision", response_model=ProvisionResponse)
async def provision_automation(
    request: ProvisionRequest,
    service_token: str = Depends(verify_service_token)
):
    """
    Provision endpoint - Called by Zimmer platform when user purchases automation
    
    This endpoint is called when a user provisions the automation.
    It should set up the user's automation instance.
    """
    try:
        # Store user automation data
        user_automations[request.user_automation_id] = {
            "user_id": request.user_id,
            "bot_token": request.bot_token,
            "demo_tokens": request.demo_tokens,
            "provisioned_at": datetime.now(timezone.utc).isoformat(),
            "status": "active"
        }
        
        # Initialize KB status for this user
        kb_status[request.user_automation_id] = {
            "status": "empty",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_documents": 0,
            "healthy": True
        }
        
        return ProvisionResponse(
            success=True,
            message="Automation provisioned successfully",
            provisioned_at=datetime.now(timezone.utc).isoformat(),
            integration_status="active",
            service_url=f"https://mock-automation.com/user/{request.user_automation_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provisioning failed: {str(e)}")

# Usage consumption endpoint (REQUIRED)
@app.post("/usage/consume", response_model=UsageConsumeResponse)
async def consume_usage(
    request: UsageConsumeRequest,
    service_token: str = Depends(verify_service_token)
):
    """
    Usage consumption endpoint - Called by Zimmer platform to consume tokens
    
    This endpoint is called when the automation performs actions that consume tokens.
    """
    try:
        # Get user automation data
        user_automation = user_automations.get(request.user_automation_id)
        if not user_automation:
            raise HTTPException(status_code=404, detail="User automation not found")
        
        # Check if user has enough tokens
        demo_tokens = user_automation.get("demo_tokens", 0)
        paid_tokens = user_automation.get("paid_tokens", 0)
        total_tokens = demo_tokens + paid_tokens
        
        if total_tokens < request.units:
            return UsageConsumeResponse(
                accepted=False,
                remaining_demo_tokens=demo_tokens,
                remaining_paid_tokens=paid_tokens,
                message="Insufficient tokens"
            )
        
        # Consume tokens (demo tokens first, then paid)
        remaining_demo = max(0, demo_tokens - request.units)
        remaining_paid = paid_tokens
        if remaining_demo == 0 and request.units > demo_tokens:
            remaining_paid = max(0, paid_tokens - (request.units - demo_tokens))
        
        # Update user automation
        user_automation["demo_tokens"] = remaining_demo
        user_automation["paid_tokens"] = remaining_paid
        
        # Log usage
        usage_logs.append({
            "user_automation_id": request.user_automation_id,
            "units": request.units,
            "usage_type": request.usage_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "meta": request.meta
        })
        
        return UsageConsumeResponse(
            accepted=True,
            remaining_demo_tokens=remaining_demo,
            remaining_paid_tokens=remaining_paid,
            message="Tokens consumed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Usage consumption failed: {str(e)}")

# KB status endpoint (REQUIRED for KB-enabled automations)
@app.get("/kb/status", response_model=KBStatusResponse)
async def get_kb_status(
    user_automation_id: int,
    service_token: str = Depends(verify_service_token)
):
    """
    Knowledge base status endpoint - Called by Zimmer platform to check KB status
    
    This endpoint returns the current status of the user's knowledge base.
    """
    try:
        kb_data = kb_status.get(user_automation_id)
        if not kb_data:
            raise HTTPException(status_code=404, detail="User automation not found")
        
        return KBStatusResponse(**kb_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"KB status check failed: {str(e)}")

# KB reset endpoint (REQUIRED for KB-enabled automations)
@app.post("/kb/reset", response_model=KBResetResponse)
async def reset_kb(
    user_automation_id: int,
    service_token: str = Depends(verify_service_token)
):
    """
    Knowledge base reset endpoint - Called by Zimmer platform to reset KB
    
    This endpoint resets the user's knowledge base to empty state.
    """
    try:
        # Reset KB status
        kb_status[user_automation_id] = {
            "status": "empty",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_documents": 0,
            "healthy": True
        }
        
        return KBResetResponse(
            success=True,
            message="Knowledge base reset successfully",
            reset_at=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"KB reset failed: {str(e)}")

# Additional endpoints for testing and monitoring
@app.get("/status")
async def get_service_status():
    """Get detailed service status"""
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "uptime": int(time.time() - START_TIME),
        "active_users": len(user_automations),
        "total_usage_events": len(usage_logs),
        "status": "operational"
    }

@app.get("/users")
async def list_users(service_token: str = Depends(verify_service_token)):
    """List all provisioned users (for testing)"""
    return {
        "users": list(user_automations.keys()),
        "total": len(user_automations)
    }

@app.get("/usage/logs")
async def get_usage_logs(service_token: str = Depends(verify_service_token)):
    """Get usage logs (for testing)"""
    return {
        "logs": usage_logs,
        "total": len(usage_logs)
    }

# Main execution
if __name__ == "__main__":
    print(f"🚀 Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    print("📋 Available endpoints:")
    print("  GET  /health - Health check (REQUIRED)")
    print("  POST /provision - Provision automation (REQUIRED)")
    print("  POST /usage/consume - Consume tokens (REQUIRED)")
    print("  GET  /kb/status - KB status (REQUIRED for KB automations)")
    print("  POST /kb/reset - Reset KB (REQUIRED for KB automations)")
    print("  GET  /status - Service status")
    print("  GET  /users - List users (testing)")
    print("  GET  /usage/logs - Usage logs (testing)")
    print("\n🔧 Service will run on http://localhost:8002")
    print("🔑 Use 'mock_test_token' as service token for testing")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
