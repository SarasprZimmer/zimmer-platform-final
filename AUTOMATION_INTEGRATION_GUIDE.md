# 🤖 Zimmer Platform - Automation Integration Guide

**Version:** 2.0  
**Date:** January 2025  
**Status:** ✅ TESTED & VERIFIED

## 📋 Overview

This guide provides comprehensive instructions for integrating external automation services with the Zimmer AI Platform. Based on our testing with a mock automation service, this guide covers all requirements, endpoints, API key integration, and best practices for successful integration.

## 🚀 Quick Start Guide for Developers

### Prerequisites Checklist
Before starting your automation integration, ensure you have:

- [ ] **Development Environment**: Python 3.8+ or Node.js 16+
- [ ] **Web Framework**: FastAPI (Python) or Express.js (Node.js)
- [ ] **Hosting Platform**: HTTPS-enabled server (AWS, DigitalOcean, etc.)
- [ ] **Platform Access**: Contact Zimmer platform administrator
- [ ] **Service Token**: Request from platform admin (required for authentication)

### Step 1: Project Setup (5 minutes)

#### Create Project Structure
```bash
mkdir your-automation-service
cd your-automation-service

# Python FastAPI setup
pip install fastapi uvicorn python-multipart
touch app.py requirements.txt .env

# Or Node.js Express setup
npm init -y
npm install express cors dotenv
touch app.js package.json .env
```

#### Basic Project Files
```python
# requirements.txt (Python)
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
requests==2.31.0
```

```json
// package.json (Node.js)
{
  "name": "your-automation-service",
  "version": "1.0.0",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }
}
```

### Step 2: Implement Health Check (10 minutes)

#### Python FastAPI Implementation
```python
# app.py
from fastapi import FastAPI
import time

app = FastAPI(title="Your Automation Service", version="1.0.0")
START_TIME = time.time()

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": int(time.time() - START_TIME)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Node.js Express Implementation
```javascript
// app.js
const express = require('express');
const app = express();

const START_TIME = Date.now();

app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        version: '1.0.0',
        uptime: Math.floor((Date.now() - START_TIME) / 1000)
    });
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

#### Test Your Health Check
```bash
# Start your service
python app.py  # or node app.js

# Test in another terminal
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "ok",
#   "version": "1.0.0",
#   "uptime": 123
# }
```

### Step 3: Add Service Token Authentication (15 minutes)

#### Python Implementation
```python
# app.py (continued)
from fastapi import HTTPException, Header, Depends
import os

def verify_service_token(x_zimmer_service_token: str = Header(None)):
    if not x_zimmer_service_token:
        raise HTTPException(status_code=401, detail="Missing service token")
    
    # In production, validate against platform
    valid_tokens = os.getenv("VALID_SERVICE_TOKENS", "").split(",")
    if x_zimmer_service_token not in valid_tokens:
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    return x_zimmer_service_token

# Test endpoint with authentication
@app.post("/test-auth")
async def test_auth(service_token: str = Depends(verify_service_token)):
    return {"message": "Authentication successful", "token": service_token[:10] + "..."}
```

#### Node.js Implementation
```javascript
// app.js (continued)
const verifyServiceToken = (req, res, next) => {
    const token = req.headers['x-zimmer-service-token'];
    if (!token) {
        return res.status(401).json({ error: 'Missing service token' });
    }
    
    const validTokens = process.env.VALID_SERVICE_TOKENS?.split(',') || [];
    if (!validTokens.includes(token)) {
        return res.status(401).json({ error: 'Invalid service token' });
    }
    
    next();
};

app.post('/test-auth', verifyServiceToken, (req, res) => {
    res.json({ 
        message: 'Authentication successful',
        token: req.headers['x-zimmer-service-token'].substring(0, 10) + '...'
    });
});
```

#### Environment Configuration
```bash
# .env
VALID_SERVICE_TOKENS=zst_your_token_here,zst_backup_token
PLATFORM_URL=https://zimmer-platform.com
AUTOMATION_ID=123
```

### Step 4: Implement Core Endpoints (30 minutes)

#### Provision Endpoint
```python
# app.py (continued)
from pydantic import BaseModel
from typing import Optional
import time

class ProvisionRequest(BaseModel):
    user_automation_id: int
    user_id: int
    demo_tokens: int
    bot_token: Optional[str] = None

@app.post("/provision")
async def provision_automation(
    request: ProvisionRequest,
    service_token: str = Depends(verify_service_token)
):
    try:
        # Your provision logic here
        # - Set up user instance
        # - Initialize database records
        # - Configure bot (if applicable)
        
        return {
            "success": True,
            "message": "Automation provisioned successfully",
            "provisioned_at": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "integration_status": "active",
            "service_url": f"https://your-service.com/user/{request.user_automation_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provision failed: {str(e)}")
```

#### Usage Consumption Endpoint
```python
# app.py (continued)
class UsageRequest(BaseModel):
    user_automation_id: int
    units: int
    usage_type: str
    meta: Optional[dict] = None

@app.post("/usage/consume")
async def consume_usage(
    request: UsageRequest,
    service_token: str = Depends(verify_service_token)
):
    try:
        # Your token consumption logic here
        # - Check user's token balance
        # - Consume tokens
        # - Update database
        
        # Mock implementation
        remaining_demo_tokens = max(0, 5 - request.units)
        remaining_paid_tokens = 0
        
        return {
            "accepted": True,
            "remaining_demo_tokens": remaining_demo_tokens,
            "remaining_paid_tokens": remaining_paid_tokens,
            "message": "Tokens consumed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Usage consumption failed: {str(e)}")
```

### Step 5: Test Your Integration (10 minutes)

#### Create Test Script
```python
# test_integration.py
import requests
import json

def test_automation_service(base_url: str, service_token: str):
    headers = {
        "X-Zimmer-Service-Token": service_token,
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing automation service...")
    
    # Test 1: Health Check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Provision
    print("\n2️⃣ Testing provision...")
    try:
        data = {
            "user_automation_id": 999,
            "user_id": 999,
            "demo_tokens": 5
        }
        response = requests.post(f"{base_url}/provision", headers=headers, json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Provision passed")
        else:
            print(f"   ❌ Provision failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Provision error: {e}")
    
    # Test 3: Usage Consumption
    print("\n3️⃣ Testing usage consumption...")
    try:
        data = {
            "user_automation_id": 999,
            "units": 2,
            "usage_type": "chat_session"
        }
        response = requests.post(f"{base_url}/usage/consume", headers=headers, json=data, timeout=3)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Usage consumption passed")
        else:
            print(f"   ❌ Usage consumption failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Usage consumption error: {e}")

if __name__ == "__main__":
    test_automation_service(
        base_url="http://localhost:8000",
        service_token="zst_your_token_here"
    )
```

#### Run Tests
```bash
# Start your service
python app.py

# In another terminal, run tests
python test_integration.py
```

### Step 6: Deploy to Production (20 minutes)

#### Docker Setup
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  automation-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - VALID_SERVICE_TOKENS=${SERVICE_TOKENS}
      - PLATFORM_URL=${PLATFORM_URL}
    restart: unless-stopped
```

#### Deploy Commands
```bash
# Build and run with Docker
docker build -t your-automation-service .
docker run -p 8000:8000 -e VALID_SERVICE_TOKENS="zst_your_token" your-automation-service

# Or with Docker Compose
docker-compose up -d
```

### Step 7: Register with Platform (5 minutes)

1. **Contact Platform Administrator**
   - Email: admin@zimmer-platform.com
   - Provide your service URL and health check endpoint
   - Request service token for authentication

2. **Platform Registration Details**
   - Service Name: Your Automation Name
   - Base URL: https://your-automation-service.com
   - Health Check URL: https://your-automation-service.com/health
   - Pricing: $X per token or subscription model

3. **Receive Service Token**
   - Platform admin will provide your service token
   - Update your `.env` file with the token
   - Test authentication with the provided token

### Step 8: Verify Platform Integration (10 minutes)

#### Platform Health Check
```bash
# Platform will automatically check your health endpoint
# Monitor status in admin dashboard or via API

curl -X POST "https://zimmer-platform.com/api/admin/automations/{automation_id}/health-check" \
  -H "Authorization: Bearer admin_token"
```

#### Expected Success Indicators
- [ ] Health check returns 200 with required fields
- [ ] Provision endpoint works with service token
- [ ] Usage consumption manages tokens correctly
- [ ] Platform shows "healthy" status
- [ ] Automation appears in marketplace

### 🎯 Quick Start Checklist

**Development (30 minutes)**
- [ ] Project setup and basic structure
- [ ] Health check endpoint implemented
- [ ] Service token authentication added
- [ ] Core endpoints (provision, usage) implemented
- [ ] Local testing completed

**Deployment (30 minutes)**
- [ ] Docker configuration created
- [ ] Service deployed to production
- [ ] HTTPS enabled and working
- [ ] Environment variables configured
- [ ] Service accessible from internet

**Platform Integration (15 minutes)**
- [ ] Contacted platform administrator
- [ ] Received service token
- [ ] Updated configuration with token
- [ ] Platform health check passing
- [ ] Automation listed in marketplace

**Total Time: ~75 minutes**

### 🚨 Common Quick Start Issues

**Issue: Health check not accessible**
- Ensure service is running on correct port
- Check firewall settings
- Verify URL is accessible from internet

**Issue: Service token authentication fails**
- Verify token format (should start with "zst_")
- Check environment variable is set correctly
- Ensure token is in valid tokens list

**Issue: Platform health check fails**
- Check response format matches specification
- Ensure all required fields are present
- Verify response time is under 5 seconds

**Issue: Provision endpoint errors**
- Check request format matches specification
- Verify all required fields are included
- Ensure proper error handling

### 📞 Quick Support

**Need Help?**
- **Documentation**: This guide and API reference
- **Examples**: See `mock_automation_service.py` for complete implementation
- **Platform Admin**: admin@zimmer-platform.com
- **Developer Support**: #platform-support on Discord

**Emergency Issues**
- Service down: Check health status in admin dashboard
- Authentication issues: Verify service token with platform admin
- Integration problems: Review platform logs and error messages

---

## 🔑 API Key Integration Overview

The Zimmer platform provides **centralized OpenAI API key management** for all automations. This means:

- **No API Keys in Your Code**: Automations don't need to manage their own OpenAI API keys
- **Automatic Key Rotation**: Platform handles key rotation and fallback automatically  
- **Usage Tracking**: All API usage is tracked and monitored centrally
- **Cost Management**: Platform manages costs and billing for all automations
- **Load Balancing**: Multiple keys per automation for high availability

### Integration Methods

#### Method 1: Platform-Managed Keys (Recommended)
```python
# Use the platform's built-in GPT service
from zimmer_backend.services.gpt import generate_gpt_response_with_keys

response = generate_gpt_response_with_keys(
    db=db,
    message=user_message,
    automation_id=automation_id,
    user_id=user_id
)
```

#### Method 2: Direct Key Request (Advanced)
```python
# Request keys from platform and manage locally
POST /api/automations/{automation_id}/openai-key
POST /api/automations/{automation_id}/openai-usage
```

## 🎯 Integration Requirements

### Prerequisites
- Automation service must be accessible via HTTP/HTTPS
- Service must implement required endpoints (see below)
- Service must support service token authentication
- Service must respond to health checks within 5 seconds
- Service must be compatible with platform's OpenAI key management

### Service Token Authentication
- All protected endpoints require `X-Zimmer-Service-Token` header
- Service tokens are provided by the platform administrator
- Tokens are used to verify automation identity and permissions

## 🔍 Platform Validation System

The Zimmer platform includes a **comprehensive validation system** that automatically checks and reports on automation integration status:

### Health Check Validation
- **Automatic Monitoring**: Platform checks automation health every 5 minutes
- **Real-time Status**: Health status updated in real-time
- **Detailed Reporting**: Comprehensive error reporting and diagnostics
- **Purchase Gating**: Only healthy automations are available for purchase

### Validation Criteria
The platform validates automations based on:

1. **Health Check Response**:
   - HTTP status code must be 200
   - Response time must be < 5 seconds
   - Required fields must be present: `status`, `version`, `uptime`
   - Status value must be `"ok"`, `"healthy"`, or `"up"`

2. **Endpoint Functionality**:
   - All required endpoints must be accessible
   - Service token authentication must work
   - Response formats must match specifications
   - Error handling must be proper

3. **Performance Requirements**:
   - Health check: < 5 seconds
   - Provision endpoint: < 10 seconds
   - Usage consumption: < 3 seconds
   - KB operations: < 15 seconds

### Status Classification
The platform classifies automation health into three categories:

- **🟢 Healthy**: All criteria met, available for purchase
- **🟡 Degraded**: Some issues, not available for purchase
- **🔴 Unhealthy**: Major issues, not available for purchase

### Admin Health Check Endpoint
Administrators can manually trigger health checks:

```http
POST /api/admin/automations/{automation_id}/health-check
```

**Response:**
```json
{
  "automation_id": 1,
  "health_status": "healthy",
  "is_listed": true,
  "last_health_at": "2025-01-10T17:30:00Z",
  "details": {
    "ok": true,
    "body": {
      "status": "ok",
      "version": "1.0.0",
      "uptime": 12345
    }
  }
}
```

## 🔧 Required Endpoints

### 1. Health Check Endpoint (REQUIRED)

**Endpoint:** `GET /health`  
**Authentication:** None (public endpoint)  
**Timeout:** 5 seconds  
**Purpose:** Platform health monitoring and availability checking  
**Validation:** Platform automatically checks this endpoint every 5 minutes  
**Impact:** Determines if automation is available for purchase

#### Request
```http
GET /health HTTP/1.1
Host: your-automation-service.com
```

#### Required Response Format
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": 12345
}
```

#### Response Fields
- **`status`** (required): Must be `"ok"`, `"healthy"`, or `"up"` for healthy status
- **`version`** (required): Current version of the automation service
- **`uptime`** (required): Service uptime in seconds

#### Health Status Classification
- **Healthy**: HTTP 200 + required fields + status in ["ok", "healthy", "up"]
- **Degraded**: HTTP 200 + required fields + status not in healthy values
- **Unhealthy**: HTTP error, timeout, or missing required fields

#### Example Implementation
```python
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": int(time.time() - START_TIME)
    }
```

### 2. Provision Endpoint (REQUIRED)

**Endpoint:** `POST /provision`  
**Authentication:** Service token required  
**Timeout:** 10 seconds  
**Purpose:** Set up user's automation instance when purchased  
**Validation:** Platform validates response format and success status  
**Impact:** Determines if user can successfully access the automation

#### Request
```http
POST /provision HTTP/1.1
Host: your-automation-service.com
X-Zimmer-Service-Token: your_service_token
Content-Type: application/json

{
  "user_automation_id": 123,
  "user_id": 456,
  "bot_token": "optional_telegram_bot_token",
  "demo_tokens": 5
}
```

#### Request Fields
- **`user_automation_id`** (required): Unique ID for this user's automation instance
- **`user_id`** (required): Platform user ID
- **`bot_token`** (optional): Telegram bot token if applicable
- **`demo_tokens`** (required): Number of demo tokens allocated

#### Response Format
```json
{
  "success": true,
  "message": "Automation provisioned successfully",
  "provisioned_at": "2025-01-10T16:54:49.650619+00:00",
  "integration_status": "active",
  "service_url": "https://your-automation.com/user/123"
}
```

#### Response Fields
- **`success`** (required): Boolean indicating success
- **`message`** (required): Human-readable status message
- **`provisioned_at`** (required): ISO timestamp of provisioning
- **`integration_status`** (required): Status of integration ("active", "pending", "failed")
- **`service_url`** (optional): URL for user to access their automation

### 3. Usage Consumption Endpoint (REQUIRED)

**Endpoint:** `POST /usage/consume`  
**Authentication:** Service token required  
**Timeout:** 3 seconds  
**Purpose:** Consume tokens when automation performs actions  
**Validation:** Platform validates token consumption and remaining balances  
**Impact:** Controls user access based on available tokens

#### Request
```http
POST /usage/consume HTTP/1.1
Host: your-automation-service.com
X-Zimmer-Service-Token: your_service_token
Content-Type: application/json

{
  "user_automation_id": 123,
  "units": 2,
  "usage_type": "chat_session",
  "meta": {
    "session_id": "abc123",
    "message_count": 5
  }
}
```

#### Request Fields
- **`user_automation_id`** (required): User's automation instance ID
- **`units`** (required): Number of tokens to consume
- **`usage_type`** (required): Type of usage ("chat_session", "api_call", etc.)
- **`meta`** (optional): Additional metadata about the usage

#### Response Format
```json
{
  "accepted": true,
  "remaining_demo_tokens": 3,
  "remaining_paid_tokens": 0,
  "message": "Tokens consumed successfully"
}
```

#### Response Fields
- **`accepted`** (required): Boolean indicating if consumption was accepted
- **`remaining_demo_tokens`** (required): Remaining demo tokens
- **`remaining_paid_tokens`** (required): Remaining paid tokens
- **`message`** (required): Status message

### 4. Knowledge Base Status Endpoint (REQUIRED for KB-enabled automations)

**Endpoint:** `GET /kb/status`  
**Authentication:** Service token required  
**Timeout:** 15 seconds  
**Purpose:** Check knowledge base status for user  
**Validation:** Platform validates KB health and document counts  
**Impact:** Determines KB functionality and user experience

#### Request
```http
GET /kb/status?user_automation_id=123 HTTP/1.1
Host: your-automation-service.com
X-Zimmer-Service-Token: your_service_token
```

#### Response Format
```json
{
  "status": "ready",
  "last_updated": "2025-01-10T16:54:49.650619+00:00",
  "total_documents": 15,
  "healthy": true
}
```

#### Response Fields
- **`status`** (required): KB status ("empty", "ready", "processing", "error")
- **`last_updated`** (required): ISO timestamp of last update
- **`total_documents`** (required): Number of documents in KB
- **`healthy`** (required): Boolean indicating KB health

### 5. Knowledge Base Reset Endpoint (REQUIRED for KB-enabled automations)

**Endpoint:** `POST /kb/reset`  
**Authentication:** Service token required  
**Timeout:** 15 seconds  
**Purpose:** Reset user's knowledge base to empty state  
**Validation:** Platform validates reset success and KB state  
**Impact:** Allows users to start fresh with their knowledge base

#### Request
```http
POST /kb/reset?user_automation_id=123 HTTP/1.1
Host: your-automation-service.com
X-Zimmer-Service-Token: your_service_token
```

#### Response Format
```json
{
  "success": true,
  "message": "Knowledge base reset successfully",
  "reset_at": "2025-01-10T16:54:55.806249+00:00"
}
```

## 🔐 Authentication & Security

### Service Token Implementation
```python
from fastapi import HTTPException, Header

def verify_service_token(x_zimmer_service_token: str = Header(None)):
    if not x_zimmer_service_token:
        raise HTTPException(status_code=401, detail="Missing service token")
    
    # Verify token against platform (implement your verification logic)
    if not is_valid_token(x_zimmer_service_token):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    return x_zimmer_service_token

# Use in endpoints
@app.post("/provision")
async def provision_automation(
    request: ProvisionRequest,
    service_token: str = Depends(verify_service_token)
):
    # Your implementation
    pass
```

### Security Best Practices
- Always validate service tokens
- Use HTTPS in production
- Implement rate limiting
- Log all API calls for monitoring
- Validate all input data
- Use proper HTTP status codes

## 📊 Platform Integration Process

### 1. Automation Registration
1. Contact platform administrator to register your automation
2. Provide automation details:
   - Service name and description
   - Base URL and health check URL
   - Pricing information
   - Required endpoints list
3. Receive service token for authentication

### 2. Health Check Setup
1. Implement `/health` endpoint
2. Ensure response includes all required fields
3. Test endpoint accessibility from platform
4. Verify response time is under 5 seconds

### 3. Endpoint Implementation
1. Implement all required endpoints
2. Add service token authentication
3. Test each endpoint thoroughly
4. Implement proper error handling

### 4. Platform Testing
1. Platform administrator runs health checks
2. Test provision and usage consumption
3. Verify KB endpoints (if applicable)
4. Confirm integration status

## 🧪 Testing Your Integration

### Health Check Test
```bash
curl -X GET "https://your-automation.com/health"
```

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": 12345
}
```

### Provision Test
```bash
curl -X POST "https://your-automation.com/provision" \
  -H "X-Zimmer-Service-Token: your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_automation_id": 1,
    "user_id": 1,
    "demo_tokens": 5
  }'
```

### Usage Consumption Test
```bash
curl -X POST "https://your-automation.com/usage/consume" \
  -H "X-Zimmer-Service-Token: your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_automation_id": 1,
    "units": 2,
    "usage_type": "chat_session"
  }'
```

## 📈 Monitoring & Maintenance

### Platform Validation & Reporting System

The Zimmer platform includes a **comprehensive validation and reporting system** that provides detailed insights into automation integration status:

#### 1. **Automatic Health Monitoring**
- **Frequency**: Platform checks automation health every 5 minutes
- **Real-time Updates**: Health status updated immediately after each check
- **Purchase Gating**: Only healthy automations are available for purchase
- **Marketplace Visibility**: Unhealthy automations are hidden from users

#### 2. **Detailed Status Reporting**

**Health Status Levels:**
- **🟢 Healthy**: All endpoints working, response times good, all criteria met
- **🟡 Degraded**: Some issues detected, but basic functionality works
- **🔴 Unhealthy**: Major issues, automation not available for purchase

**Validation Metrics Tracked:**
- Response times for each endpoint
- Success/failure rates
- Error types and frequencies
- API key availability and usage
- Token consumption patterns

#### 3. **Admin Dashboard Integration**

Administrators can monitor automation health through:

**Manual Health Check:**
```http
POST /api/admin/automations/{automation_id}/health-check
```

**Comprehensive Status Report:**
```json
{
  "automation_id": 1,
  "health_status": "healthy",
  "is_listed": true,
  "last_health_at": "2025-01-10T17:30:00Z",
  "response_times": {
    "health_check": 0.5,
    "provision": 2.1,
    "usage_consume": 0.8,
    "kb_status": 1.2
  },
  "success_rates": {
    "health_check": 100,
    "provision": 98.5,
    "usage_consume": 99.2,
    "kb_status": 95.8
  },
  "openai_key_status": {
    "total_keys": 3,
    "active_keys": 3,
    "exhausted_keys": 0,
    "daily_usage": 1250
  },
  "details": {
    "ok": true,
    "body": {
      "status": "ok",
      "version": "1.0.0",
      "uptime": 12345
    }
  }
}
```

#### 4. **Real-time Alerts**

The platform can send alerts for:
- Health check failures
- Response time degradation
- API key exhaustion
- High error rates
- Service downtime

#### 5. **Performance Analytics**

Track these metrics over time:
- Average response times per endpoint
- Success/failure trends
- Peak usage patterns
- Cost per automation
- User satisfaction scores

### Health Monitoring
- Platform automatically checks health every 5 minutes
- Unhealthy automations are removed from marketplace
- Health status affects user purchase availability

### Performance Requirements
- Health check response time: < 5 seconds
- Provision endpoint: < 10 seconds
- Usage consumption: < 3 seconds
- KB operations: < 15 seconds

### Error Handling
- Return appropriate HTTP status codes
- Provide clear error messages
- Log errors for debugging
- Implement retry logic for transient failures

## 🔑 API Key Integration Criteria

### OpenAI Key Management Requirements

To integrate with the platform's OpenAI key management system, your automation must meet these criteria:

#### 1. **No Direct API Key Management**
- ❌ **Don't**: Store OpenAI API keys in your automation code
- ❌ **Don't**: Hardcode API keys in environment variables
- ❌ **Don't**: Manage key rotation manually
- ✅ **Do**: Use the platform's centralized key management

#### 2. **Integration Method Selection**

**Method 1: Platform-Managed (Recommended)**
```python
# Your automation uses the platform's GPT service
from zimmer_backend.services.gpt import generate_gpt_response_with_keys

def handle_user_message(message: str, user_id: int, automation_id: int):
    response = generate_gpt_response_with_keys(
        db=db,
        message=message,
        automation_id=automation_id,
        user_id=user_id
    )
    return response
```

**Method 2: Direct Key Request (Advanced)**
```python
# Your automation requests keys from platform
async def get_openai_key(automation_id: int):
    response = await requests.post(
        f"{PLATFORM_URL}/api/automations/{automation_id}/openai-key",
        headers={"X-Zimmer-Service-Token": SERVICE_TOKEN}
    )
    return response.json()

async def report_usage(automation_id: int, key_id: int, tokens: int):
    await requests.post(
        f"{PLATFORM_URL}/api/automations/{automation_id}/openai-usage",
        headers={"X-Zimmer-Service-Token": SERVICE_TOKEN},
        json={"key_id": key_id, "tokens_used": tokens}
    )
```

#### 3. **Key Request Endpoints (Method 2 Only)**

**Request OpenAI Key:**
```http
POST /api/automations/{automation_id}/openai-key
X-Zimmer-Service-Token: your_service_token
Content-Type: application/json

{
  "model": "gpt-4",
  "max_tokens": 150
}
```

**Response:**
```json
{
  "success": true,
  "key_id": 123,
  "api_key": "sk-...",
  "model": "gpt-4",
  "expires_at": "2025-01-11T00:00:00Z",
  "usage_limits": {
    "rpm_limit": 60,
    "daily_token_limit": 100000
  }
}
```

**Report Usage:**
```http
POST /api/automations/{automation_id}/openai-usage
X-Zimmer-Service-Token: your_service_token
Content-Type: application/json

{
  "key_id": 123,
  "tokens_used": 45,
  "model": "gpt-4",
  "prompt_tokens": 20,
  "completion_tokens": 25,
  "success": true
}
```

#### 4. **Key Management Features**

The platform provides these features automatically:

- **🔄 Automatic Key Rotation**: Keys are rotated when they fail or exceed limits
- **⚖️ Load Balancing**: Multiple keys per automation for high availability
- **📊 Usage Tracking**: All API usage is tracked and monitored
- **💰 Cost Management**: Centralized cost tracking and billing
- **🛡️ Security**: Keys are encrypted and stored securely
- **📈 Performance**: Optimized key selection based on usage patterns

#### 5. **Error Handling**

Your automation must handle these key-related scenarios:

```python
try:
    response = generate_gpt_response_with_keys(...)
    return response
except OpenAIKeyExhaustedError:
    # Platform will automatically try next key
    return "Service temporarily unavailable, please try again"
except OpenAIKeyRotationError:
    # Platform is rotating keys
    return "Service updating, please try again in a moment"
except Exception as e:
    # Log error and provide fallback
    logger.error(f"GPT generation failed: {e}")
    return "I'm having trouble processing your request right now"
```

#### 6. **Validation Criteria**

The platform validates API key integration based on:

- **Key Availability**: At least one active key must be available
- **Usage Reporting**: Usage must be reported back to platform
- **Error Handling**: Proper handling of key failures and rotation
- **Performance**: API calls must complete within reasonable time
- **Security**: No API keys should be exposed in logs or responses

## 🔄 Data Flow Examples

### User Purchase Flow
1. User purchases automation on platform
2. Platform calls `/provision` endpoint
3. Automation sets up user instance
4. Platform updates user's automation status
5. User can now use the automation

### Token Consumption Flow
1. User interacts with automation
2. Automation calls `/usage/consume` endpoint
3. Platform validates and consumes tokens
4. Platform returns remaining token counts
5. Automation continues or stops based on tokens

### Health Check Flow
1. Platform calls `/health` endpoint every 5 minutes
2. Automation returns health status
3. Platform classifies health (healthy/degraded/unhealthy)
4. Platform updates automation listing status
5. Unhealthy automations are hidden from marketplace

## 🚨 Common Issues & Solutions

### Health Check Failures
**Issue:** Health check returns 500 error  
**Solution:** Check service status, database connectivity, and dependencies

**Issue:** Missing required fields in health response  
**Solution:** Ensure response includes `status`, `version`, and `uptime` fields

### Authentication Issues
**Issue:** 401 Unauthorized errors  
**Solution:** Verify service token is correct and properly passed in header

**Issue:** Token validation failures  
**Solution:** Check token format and validation logic

### Provision Failures
**Issue:** Provision endpoint returns error  
**Solution:** Check user data validation and database connectivity

**Issue:** Integration status not updating  
**Solution:** Ensure response includes correct `integration_status` field

## 📚 Example Implementation

See `mock_automation_service.py` for a complete working example of an automation service that integrates with the Zimmer platform.

### Key Features of Example
- ✅ Complete health check implementation
- ✅ Service token authentication
- ✅ All required endpoints
- ✅ Proper error handling
- ✅ Token consumption logic
- ✅ KB management (if applicable)
- ✅ Comprehensive testing

## 🎯 Success Criteria

Your automation integration is successful when:

### Core Integration Requirements
1. ✅ Health check endpoint returns 200 with required fields
2. ✅ Provision endpoint successfully sets up user instances
3. ✅ Usage consumption properly manages tokens
4. ✅ KB endpoints work correctly (if applicable)
5. ✅ Service token authentication is secure
6. ✅ All endpoints respond within time limits

### API Key Integration Requirements
7. ✅ OpenAI key integration implemented (Method 1 or 2)
8. ✅ No hardcoded API keys in automation code
9. ✅ Proper error handling for key failures
10. ✅ Usage reporting back to platform (Method 2)
11. ✅ Key rotation and fallback working correctly
12. ✅ Platform validation shows "healthy" status

### Platform Validation Status
13. ✅ Platform health check shows "healthy" status
14. ✅ Automation appears in marketplace for purchase
15. ✅ All validation criteria met in admin dashboard
16. ✅ Response times within acceptable limits
17. ✅ Success rates above 95% for all endpoints
18. ✅ No critical errors in platform logs

### Production Readiness
19. ✅ Comprehensive error handling implemented
20. ✅ Logging and monitoring in place
21. ✅ Performance optimized for expected load
22. ✅ Security best practices followed
23. ✅ Documentation complete and up-to-date
24. ✅ Testing completed with real platform integration

## 📞 Support

For integration support:
- Review this guide thoroughly
- Test with the provided mock service example
- Contact platform administrators for service token setup
- Use the testing endpoints to verify your implementation

---

**Last Updated:** January 2025  
**Status:** ✅ VERIFIED WITH LIVE TESTING  
**Next Review:** As needed for platform updates run d