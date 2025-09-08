# 🤖 Zimmer AI Platform - Automation Integration Guide

## Overview

The Zimmer AI Platform is designed as a **marketplace and management system** for external automation services. This guide provides comprehensive documentation for developers who want to integrate their automation services with the Zimmer platform.

## 🏗️ System Architecture

### How It Works

1. **External Automation Services** - Your automation runs independently
2. **Zimmer Platform** - Acts as a marketplace and management layer
3. **User Interface** - Users discover, purchase, and manage automations
4. **API Integration** - Secure communication between Zimmer and your service

### Key Components

- **Marketplace** - Users browse and purchase automations
- **User Management** - Account creation, authentication, billing
- **Health Monitoring** - Continuous monitoring of automation health
- **Usage Tracking** - Token consumption and billing
- **Knowledge Base** - User-specific data management

## 🔌 Required API Endpoints

Your automation service must implement the following endpoints:

### 1. Health Check Endpoint

**Purpose**: Monitor automation health and availability

**Endpoint**: `GET /health`

**Response Format**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": 12345,
  "services": ["service1", "service2"]
}
```

**Required Fields**:
- `status`: Must be `"ok"`, `"healthy"`, or `"up"` for healthy status
- `version`: Current version of your automation
- `uptime`: Service uptime in seconds

**Optional Fields**:
- `services`: Array of available services
- `maintenance_mode`: Boolean indicating maintenance status
- Any additional health metrics

### 2. User Provisioning Endpoint

**Purpose**: Set up a new user with your automation service

**Endpoint**: `POST /api/provision`

**Headers**:
```
X-Zimmer-Service-Token: <service_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "user_automation_id": 123,
  "user_id": 456,
  "bot_token": "telegram_bot_token_here",
  "demo_tokens": 5
}
```

**Response Format**:
```json
{
  "status": "success",
  "message": "User provisioned successfully",
  "webhook_url": "https://your-service.com/webhook/123",
  "user_config": {
    "max_tokens": 1000,
    "features": ["feature1", "feature2"]
  }
}
```

### 3. Usage Tracking Endpoint

**Purpose**: Track token consumption and usage

**Endpoint**: `POST /api/usage`

**Headers**:
```
X-Zimmer-Service-Token: <service_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "user_automation_id": 123,
  "units": 10,
  "usage_type": "message_processing",
  "meta": {
    "message_length": 150,
    "complexity": "medium"
  }
}
```

**Response Format**:
```json
{
  "accepted": true,
  "remaining_demo_tokens": 3,
  "remaining_paid_tokens": 500,
  "message": "Usage recorded successfully"
}
```

### 4. Knowledge Base Status Endpoint

**Purpose**: Monitor user's knowledge base health

**Endpoint**: `POST /api/kb-status`

**Headers**:
```
X-Zimmer-Service-Token: <service_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "user_id": 456,
  "user_automation_id": 123
}
```

**Response Format**:
```json
{
  "status": "healthy",
  "last_updated": "2025-01-28T15:30:00Z",
  "backup_status": true,
  "error_logs": [],
  "supports_reset": true,
  "kb_size": 1250
}
```

### 5. Knowledge Base Reset Endpoint

**Purpose**: Reset user's knowledge base

**Endpoint**: `POST /api/kb-reset`

**Headers**:
```
X-Zimmer-Service-Token: <service_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "user_automation_id": 123
}
```

**Response Format**:
```json
{
  "status": "success",
  "message": "KB reset initiated",
  "timestamp": "2025-01-28T15:30:00Z"
}
```

## 🔐 Authentication & Security

### Service Token Authentication

All API calls from Zimmer to your automation use a service token:

1. **Token Generation**: Zimmer generates a unique service token for your automation
2. **Token Storage**: Token is stored securely in environment variables
3. **Token Verification**: Your service must verify the token on each request

**Environment Variable Format**:
```
AUTOMATION_{automation_id}_SERVICE_TOKEN=your_secret_token_here
```

**Token Verification Example**:
```python
import hashlib
import hmac

def verify_service_token(received_token, expected_hash):
    """Verify the service token"""
    computed_hash = hashlib.sha256(received_token.encode()).hexdigest()
    return hmac.compare_digest(computed_hash, expected_hash)
```

## 📊 Pricing Models

The platform supports three pricing models:

### 1. Token Per Session
- User pays a fixed amount per session/chat
- Suitable for conversational AI services
- Example: 50 tokens per customer support session

### 2. Token Per Step
- User pays based on individual operations
- Suitable for multi-step processes
- Example: 25 tokens per SEO analysis step

### 3. Flat Fee
- User pays a fixed amount regardless of usage
- Suitable for subscription-based services
- Example: 1000 tokens for unlimited monthly access

## 🏥 Health Monitoring

### Health Status Classification

The platform automatically classifies your automation's health:

- **Healthy** (`healthy`): Available for purchase and use
- **Degraded** (`degraded`): Not available for purchase
- **Unhealthy** (`unhealthy`): Not available for purchase

### Health Check Requirements

- **Response Time**: Must respond within 5 seconds
- **HTTP Status**: Must return 200 for healthy state
- **Required Fields**: Must include `status`, `version`, `uptime`
- **Availability**: Must be accessible 24/7

### Health Check Best Practices

1. **Lightweight**: Keep health checks fast and simple
2. **Comprehensive**: Include essential service metrics
3. **Reliable**: Use appropriate HTTP status codes
4. **Informative**: Provide useful error messages

## 🚀 Integration Steps

### Step 1: Prepare Your Service

1. **Implement Required Endpoints**: All 5 endpoints listed above
2. **Set Up Authentication**: Service token verification
3. **Configure Health Checks**: Implement `/health` endpoint
4. **Test Locally**: Ensure all endpoints work correctly

### Step 2: Register with Zimmer

1. **Contact Admin**: Request automation registration
2. **Provide Information**:
   - Service name and description
   - API endpoints
   - Pricing model and rates
   - Health check URL
3. **Get Service Token**: Receive your unique service token

### Step 3: Configure Environment

1. **Set Service Token**: Add to your environment variables
2. **Update Endpoints**: Ensure all URLs are accessible
3. **Test Integration**: Verify all endpoints work with Zimmer

### Step 4: Go Live

1. **Health Check**: Ensure health status is "healthy"
2. **User Testing**: Test with real users
3. **Monitor Performance**: Watch health status and usage

## 📝 Example Implementation

### Python FastAPI Example

```python
from fastapi import FastAPI, HTTPException, Header
import hashlib
import hmac
import os
from datetime import datetime

app = FastAPI()

# Service token verification
def verify_token(received_token: str) -> bool:
    expected_token = os.getenv("ZIMMER_SERVICE_TOKEN")
    if not expected_token:
        return False
    return hmac.compare_digest(received_token, expected_token)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime": 86400,
        "services": ["chat", "analysis", "recommendations"]
    }

@app.post("/api/provision")
async def provision_user(
    data: dict,
    x_zimmer_service_token: str = Header(..., alias="X-Zimmer-Service-Token")
):
    """Provision a new user"""
    if not verify_token(x_zimmer_service_token):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    user_id = data["user_id"]
    bot_token = data["bot_token"]
    
    # Your provisioning logic here
    # Set up user in your system
    
    return {
        "status": "success",
        "message": "User provisioned successfully",
        "webhook_url": f"https://your-service.com/webhook/{user_id}",
        "user_config": {
            "max_tokens": 1000,
            "features": ["chat", "analysis"]
        }
    }

@app.post("/api/usage")
async def track_usage(
    data: dict,
    x_zimmer_service_token: str = Header(..., alias="X-Zimmer-Service-Token")
):
    """Track usage and token consumption"""
    if not verify_token(x_zimmer_service_token):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    # Your usage tracking logic here
    
    return {
        "accepted": True,
        "remaining_demo_tokens": 3,
        "remaining_paid_tokens": 500,
        "message": "Usage recorded successfully"
    }

@app.post("/api/kb-status")
async def kb_status(
    data: dict,
    x_zimmer_service_token: str = Header(..., alias="X-Zimmer-Service-Token")
):
    """Check knowledge base status"""
    if not verify_token(x_zimmer_service_token):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    # Your KB status logic here
    
    return {
        "status": "healthy",
        "last_updated": datetime.utcnow().isoformat(),
        "backup_status": True,
        "error_logs": [],
        "supports_reset": True,
        "kb_size": 1250
    }

@app.post("/api/kb-reset")
async def kb_reset(
    data: dict,
    x_zimmer_service_token: str = Header(..., alias="X-Zimmer-Service-Token")
):
    """Reset knowledge base"""
    if not verify_token(x_zimmer_service_token):
        raise HTTPException(status_code=401, detail="Invalid service token")
    
    # Your KB reset logic here
    
    return {
        "status": "success",
        "message": "KB reset initiated",
        "timestamp": datetime.utcnow().isoformat()
    }
```

## 🧪 Testing Your Integration

### 1. Local Testing

```bash
# Test health endpoint
curl -X GET "https://your-automation.com/health"

# Test provision endpoint
curl -X POST "https://your-automation.com/api/provision" \
  -H "X-Zimmer-Service-Token: your_token" \
  -H "Content-Type: application/json" \
  -d '{"user_automation_id": 123, "user_id": 456, "bot_token": "test_token", "demo_tokens": 5}'
```

### 2. Zimmer Integration Testing

1. **Register Your Automation**: Contact admin to add your automation
2. **Health Check**: Ensure health status is "healthy"
3. **User Testing**: Create test user and provision automation
4. **Usage Testing**: Test token consumption and tracking

## 📋 Checklist for Integration

### Pre-Integration
- [ ] All 5 required endpoints implemented
- [ ] Service token authentication working
- [ ] Health check endpoint responding correctly
- [ ] Error handling implemented
- [ ] Logging configured

### Integration
- [ ] Automation registered with Zimmer
- [ ] Service token configured
- [ ] Health status shows "healthy"
- [ ] User provisioning working
- [ ] Usage tracking functional

### Post-Integration
- [ ] Real user testing completed
- [ ] Performance monitoring set up
- [ ] Error alerts configured
- [ ] Documentation updated

## 🚨 Common Issues & Solutions

### 1. Health Check Failures

**Problem**: Health status shows "unhealthy"
**Solutions**:
- Check endpoint accessibility
- Verify response format
- Ensure required fields are present
- Check response time (< 5 seconds)

### 2. Authentication Errors

**Problem**: 401 Unauthorized errors
**Solutions**:
- Verify service token is correct
- Check token verification logic
- Ensure header name is exact: `X-Zimmer-Service-Token`

### 3. Provisioning Failures

**Problem**: User provisioning fails
**Solutions**:
- Check request body format
- Verify all required fields
- Ensure bot token is valid
- Check error logs

### 4. Usage Tracking Issues

**Problem**: Usage not being tracked
**Solutions**:
- Verify endpoint is called correctly
- Check token consumption logic
- Ensure response format is correct
- Monitor for errors

## 📞 Support & Resources

### Getting Help

1. **Documentation**: This guide and platform documentation
2. **Admin Support**: Contact platform administrators
3. **Community**: Join developer community forums
4. **Technical Support**: For integration issues

### Useful Resources

- **API Documentation**: Platform API reference
- **Health Monitoring**: Health check requirements
- **Pricing Guide**: Pricing model explanations
- **Security Guide**: Authentication and security best practices

## 🎯 Best Practices

### 1. Performance
- Keep health checks lightweight
- Implement proper caching
- Use efficient data structures
- Monitor response times

### 2. Security
- Always verify service tokens
- Use HTTPS for all endpoints
- Implement rate limiting
- Log security events

### 3. Reliability
- Implement proper error handling
- Use retry mechanisms
- Monitor service health
- Have backup systems

### 4. User Experience
- Provide clear error messages
- Implement graceful degradation
- Monitor user satisfaction
- Regular updates and improvements

---

**Ready to integrate?** Follow this guide step by step, and you'll have your automation service running on the Zimmer AI Platform in no time! 🚀
