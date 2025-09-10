#!/usr/bin/env python3
"""
Enhanced Mock Automation Service with OpenAI Key Integration

This service demonstrates how to integrate with the Zimmer platform's
OpenAI key management system, including key rotation and fallback logic.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import time
import hashlib
import hmac
import json
import httpx
import asyncio
from datetime import datetime, timezone

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced Mock Automation Service",
    description="Mock automation service with OpenAI key integration for Zimmer platform",
    version="2.0.0"
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
SERVICE_NAME = "Enhanced Travel Agency AI"
SERVICE_VERSION = "2.0.0"
START_TIME = time.time()

# Mock data storage
user_automations = {}
kb_status = {}
usage_logs = []
openai_keys = {}  # Store API keys provided by platform

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: int
    service: str
    timestamp: str
    openai_keys_available: int

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

class OpenAIKeyRequest(BaseModel):
    automation_id: int
    model: str = "gpt-4"
    max_tokens: int = 150

class OpenAIKeyResponse(BaseModel):
    success: bool
    api_key: Optional[str] = None
    key_id: Optional[int] = None
    model: str
    message: str

class GPTRequest(BaseModel):
    user_automation_id: int
    message: str
    model: str = "gpt-4"
    max_tokens: int = 150
    temperature: float = 0.7

class GPTResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    tokens_used: int = 0
    model: str
    key_id: Optional[int] = None
    message: str

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
        timestamp=datetime.now(timezone.utc).isoformat(),
        openai_keys_available=len(openai_keys)
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
            "paid_tokens": 0,
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

# NEW: OpenAI Key Management Endpoints

@app.post("/openai/request-key", response_model=OpenAIKeyResponse)
async def request_openai_key(
    request: OpenAIKeyRequest,
    service_token: str = Depends(verify_service_token)
):
    """
    Request an OpenAI API key from the platform
    
    This endpoint demonstrates how an automation would request an API key
    from the Zimmer platform's key management system.
    """
    try:
        # In a real implementation, this would call the platform's key management API
        # For this mock, we'll simulate the platform providing a key
        
        # Simulate requesting key from platform
        platform_response = await request_key_from_platform(request.automation_id, service_token)
        
        if platform_response["success"]:
            # Store the key for this automation
            key_id = platform_response["key_id"]
            openai_keys[key_id] = {
                "automation_id": request.automation_id,
                "api_key": platform_response["api_key"],
                "model": request.model,
                "max_tokens": request.max_tokens,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_used": None,
                "usage_count": 0
            }
            
            return OpenAIKeyResponse(
                success=True,
                api_key=platform_response["api_key"],
                key_id=key_id,
                model=request.model,
                message="OpenAI key provided successfully"
            )
        else:
            return OpenAIKeyResponse(
                success=False,
                message=platform_response["message"]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Key request failed: {str(e)}")

@app.post("/openai/generate", response_model=GPTResponse)
async def generate_gpt_response(
    request: GPTRequest,
    service_token: str = Depends(verify_service_token)
):
    """
    Generate GPT response using platform-managed API keys
    
    This endpoint demonstrates how an automation would use OpenAI API keys
    provided by the platform, with automatic key rotation and fallback.
    """
    try:
        # Get user automation data
        user_automation = user_automations.get(request.user_automation_id)
        if not user_automation:
            raise HTTPException(status_code=404, detail="User automation not found")
        
        print(f"DEBUG: Processing GPT request for user_automation_id={request.user_automation_id}")
        print(f"DEBUG: Available openai_keys: {list(openai_keys.keys())}")
        
        # Find available API key for this automation
        # Note: In a real implementation, we would look up the automation_id from user_automation_id
        # For this mock, we'll use the user_automation_id directly
        available_key = None
        available_key_id = None
        for key_id, key_data in openai_keys.items():
            if key_data["automation_id"] == request.user_automation_id:
                available_key = key_data
                available_key_id = key_id
                break
        
        print(f"DEBUG: Found key: {available_key_id}, Key data: {available_key}")
        
        if not available_key:
            return GPTResponse(
                success=False,
                response=None,
                tokens_used=0,
                model=request.model,
                key_id=None,
                message="No OpenAI API key available. Please request a key first."
            )
        
        # Mock OpenAI API call (since we're using mock keys)
        # In a real implementation, this would make an actual API call
        try:
            # Simulate API call delay
            await asyncio.sleep(0.1)
            
            # Mock response based on the input message
            mock_responses = {
                "hello": "Hello! I'm your travel assistant. How can I help you plan your trip today?",
                "paris": "Paris is a beautiful city! I can help you plan your visit to the City of Light. What would you like to know about Paris?",
                "weather": "I'd be happy to help with weather information! For the most accurate and up-to-date weather, I recommend checking a reliable weather service.",
                "trip": "I'd love to help you plan your trip! Could you tell me more about your destination and travel dates?",
                "help": "I'm here to assist with your travel planning needs! I can help with destinations, accommodations, activities, and more."
            }
            
            # Find the best matching response
            message_lower = request.message.lower()
            gpt_response = "I'm your travel assistant! I can help you with travel planning, destination information, and trip recommendations. How can I assist you today?"
            
            for keyword, response in mock_responses.items():
                if keyword in message_lower:
                    gpt_response = response
                    break
            
            # Simulate token usage
            tokens_used = len(request.message.split()) + len(gpt_response.split()) + 20  # Rough estimate
            
            # Update key usage
            available_key["last_used"] = datetime.now(timezone.utc).isoformat()
            available_key["usage_count"] += 1
            
            return GPTResponse(
                success=True,
                response=gpt_response,
                tokens_used=tokens_used,
                model=request.model,
                key_id=available_key_id,
                message="Response generated successfully"
            )
                    
        except Exception as e:
            return GPTResponse(
                success=False,
                response=None,
                tokens_used=0,
                model=request.model,
                key_id=None,
                message=f"Mock API error: {str(e)}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT generation failed: {str(e)}")

# Helper function to simulate platform key request
async def request_key_from_platform(automation_id: int, service_token: str) -> Dict[str, Any]:
    """
    Simulate requesting an OpenAI key from the Zimmer platform
    
    In a real implementation, this would make an HTTP request to the platform's
    key management API endpoint.
    """
    # Simulate platform response
    # In reality, this would be: POST /api/automations/{automation_id}/openai-key
    return {
        "success": True,
        "key_id": len(openai_keys) + 1,
        "api_key": f"sk-mock-key-{automation_id}-{int(time.time())}",
        "message": "Key provided successfully"
    }

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
        "openai_keys_available": len(openai_keys),
        "status": "operational"
    }

@app.get("/openai/keys")
async def list_openai_keys(service_token: str = Depends(verify_service_token)):
    """List all OpenAI keys (for testing)"""
    return {
        "keys": [
            {
                "key_id": key_id,
                "automation_id": key_data["automation_id"],
                "model": key_data["model"],
                "created_at": key_data["created_at"],
                "last_used": key_data["last_used"],
                "usage_count": key_data["usage_count"]
            }
            for key_id, key_data in openai_keys.items()
        ],
        "total": len(openai_keys)
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
    print("  POST /openai/request-key - Request OpenAI API key (NEW)")
    print("  POST /openai/generate - Generate GPT response (NEW)")
    print("  GET  /status - Service status")
    print("  GET  /openai/keys - List API keys (testing)")
    print("  GET  /users - List users (testing)")
    print("  GET  /usage/logs - Usage logs (testing)")
    print("\n🔧 Service will run on http://localhost:8003")
    print("🔑 Use 'mock_test_token' as service token for testing")
    
    uvicorn.run(app, host="0.0.0.0", port=8003)
