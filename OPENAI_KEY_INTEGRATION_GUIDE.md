# 🔑 OpenAI Key Integration Guide for Zimmer Platform

**Version:** 1.0  
**Date:** January 2025  
**Status:** ✅ TESTED & VERIFIED

## 📋 Overview

This guide explains how automations should integrate with the Zimmer platform's OpenAI key management system. The platform provides centralized key management, automatic rotation, load balancing, and fallback mechanisms for OpenAI API keys.

## 🏗️ Architecture Overview

### Platform-Side Key Management
- **Centralized Storage**: All OpenAI API keys are stored encrypted in the platform database
- **Key Pool Management**: Multiple keys per automation for load balancing and redundancy
- **Automatic Rotation**: Keys are automatically rotated when they fail or exceed limits
- **Usage Tracking**: Detailed usage monitoring and cost tracking per key
- **Rate Limiting**: Built-in rate limiting and quota management

### Automation-Side Integration
- **Key Request**: Automations request keys from the platform when needed
- **Automatic Fallback**: Platform provides fallback keys when primary keys fail
- **Usage Reporting**: Automations report usage back to the platform
- **Error Handling**: Proper error handling for key failures and rotation

## 🔧 Integration Methods

### Method 1: Platform-Managed Keys (Recommended)

The platform manages all OpenAI API keys and provides them to automations through internal services.

#### How It Works:
1. **Admin Setup**: Platform administrators add OpenAI API keys for each automation
2. **Key Pool**: Platform maintains a pool of keys per automation
3. **Automatic Selection**: Platform automatically selects the best available key
4. **Fallback Logic**: If a key fails, platform automatically tries the next key
5. **Usage Tracking**: Platform tracks all usage and costs

#### Implementation:
```python
# In your automation service
from zimmer_backend.services.gpt import generate_gpt_response_with_keys

def handle_user_message(message: str, user_id: int, automation_id: int):
    """Handle user message using platform-managed OpenAI keys"""
    
    # The platform handles all key management internally
    response = generate_gpt_response_with_keys(
        db=db,
        message=message,
        automation_id=automation_id,
        user_id=user_id
    )
    
    return response
```

### Method 2: Direct Key Request (Alternative)

Automations can request API keys directly from the platform and manage them locally.

#### Required Endpoints:

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

## 🔄 Key Management Features

### 1. Automatic Key Selection
The platform automatically selects the best available key based on:
- **Usage Load**: Keys with lower current usage are preferred
- **Health Status**: Only healthy keys are selected
- **Rate Limits**: Keys approaching rate limits are avoided
- **Daily Limits**: Keys approaching daily token limits are avoided

### 2. Automatic Fallback
When a key fails, the platform automatically:
- **Marks Key Status**: Updates key status (disabled, exhausted, error)
- **Selects Next Key**: Automatically tries the next available key
- **Retries Request**: Retries the original request with the new key
- **Logs Failures**: Records failure details for monitoring

### 3. Key Rotation
Keys are automatically rotated when:
- **Authentication Errors**: 401/403 errors indicate invalid keys
- **Rate Limit Exceeded**: 429 errors trigger key rotation
- **Daily Limit Reached**: Token limits trigger key rotation
- **Manual Rotation**: Admins can manually rotate keys

### 4. Usage Tracking
The platform tracks:
- **Token Usage**: Per-key token consumption
- **Request Count**: Number of requests per key
- **Error Rates**: Failure rates per key
- **Cost Tracking**: Estimated costs per automation
- **Performance Metrics**: Response times and latency

## 📊 Key Status Management

### Key Statuses:
- **`active`**: Key is healthy and available for use
- **`disabled`**: Key is manually disabled by admin
- **`exhausted`**: Key has reached daily token limit
- **`error`**: Key has authentication or other errors

### Status Transitions:
```
active → exhausted (daily limit reached)
active → error (authentication failure)
active → disabled (manual admin action)
exhausted → active (daily reset)
error → active (manual admin action)
```

## 🛠️ Implementation Examples

### Example 1: Simple GPT Integration
```python
from fastapi import FastAPI, Depends
from zimmer_backend.services.gpt import generate_gpt_response_with_keys

app = FastAPI()

@app.post("/chat")
async def chat_with_user(
    message: str,
    user_id: int,
    automation_id: int,
    db: Session = Depends(get_db)
):
    """Simple chat endpoint using platform-managed keys"""
    
    # Platform handles all key management
    response = generate_gpt_response_with_keys(
        db=db,
        message=message,
        automation_id=automation_id,
        user_id=user_id
    )
    
    return {"response": response}
```

### Example 2: Advanced Key Management
```python
from zimmer_backend.services.openai_key_manager import OpenAIKeyManager

class AdvancedAutomation:
    def __init__(self, db: Session):
        self.key_manager = OpenAIKeyManager(db)
    
    async def generate_response(self, message: str, automation_id: int, user_id: int):
        """Advanced response generation with manual key management"""
        
        max_retries = 3
        for attempt in range(max_retries):
            # Get the best available key
            key = self.key_manager.select_key(automation_id)
            if not key:
                return "Service temporarily unavailable"
            
            try:
                # Decrypt the key
                decrypted_key = decrypt_secret(key.key_encrypted)
                
                # Make OpenAI API call
                client = openai.OpenAI(api_key=decrypted_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": message}],
                    max_tokens=150
                )
                
                # Record successful usage
                self.key_manager.record_usage(
                    key_id=key.id,
                    tokens_used=response.usage.total_tokens,
                    ok=True,
                    model=response.model,
                    automation_id=automation_id,
                    user_id=user_id
                )
                
                return response.choices[0].message.content
                
            except openai.AuthenticationError:
                # Handle auth errors
                self.key_manager.handle_failure(key.id, "401")
                continue
                
            except openai.RateLimitError:
                # Handle rate limits
                self.key_manager.handle_failure(key.id, "429")
                continue
                
            except Exception as e:
                # Handle other errors
                self.key_manager.handle_failure(key.id, "unknown")
                continue
        
        return "Service temporarily unavailable"
```

### Example 3: Key Request Integration
```python
import httpx

class KeyRequestAutomation:
    def __init__(self, platform_base_url: str, service_token: str):
        self.platform_url = platform_base_url
        self.service_token = service_token
        self.current_key = None
    
    async def request_openai_key(self, automation_id: int):
        """Request an OpenAI key from the platform"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.platform_url}/api/automations/{automation_id}/openai-key",
                headers={"X-Zimmer-Service-Token": self.service_token},
                json={"model": "gpt-4", "max_tokens": 150}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.current_key = data
                return data
            else:
                raise Exception(f"Key request failed: {response.status_code}")
    
    async def generate_response(self, message: str, automation_id: int):
        """Generate response using requested key"""
        
        if not self.current_key:
            await self.request_openai_key(automation_id)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.current_key['api_key']}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.current_key["model"],
                        "messages": [{"role": "user", "content": message}],
                        "max_tokens": self.current_key["max_tokens"]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Report usage back to platform
                    await self.report_usage(
                        automation_id,
                        self.current_key["key_id"],
                        data["usage"]["total_tokens"],
                        True
                    )
                    
                    return data["choices"][0]["message"]["content"]
                else:
                    # Report failure
                    await self.report_usage(
                        automation_id,
                        self.current_key["key_id"],
                        0,
                        False,
                        str(response.status_code)
                    )
                    
                    # Request new key
                    await self.request_openai_key(automation_id)
                    return await self.generate_response(message, automation_id)
                    
        except Exception as e:
            # Report failure and request new key
            await self.report_usage(
                automation_id,
                self.current_key["key_id"],
                0,
                False,
                str(e)
            )
            await self.request_openai_key(automation_id)
            raise e
    
    async def report_usage(self, automation_id: int, key_id: int, tokens: int, success: bool, error: str = None):
        """Report usage back to platform"""
        
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.platform_url}/api/automations/{automation_id}/openai-usage",
                headers={"X-Zimmer-Service-Token": self.service_token},
                json={
                    "key_id": key_id,
                    "tokens_used": tokens,
                    "success": success,
                    "error": error
                }
            )
```

## 🔐 Security Considerations

### 1. Key Encryption
- All API keys are encrypted at rest in the database
- Keys are only decrypted when needed for API calls
- Encryption keys are managed separately from application keys

### 2. Access Control
- Only authorized automations can request keys
- Service tokens are required for all key requests
- Keys are scoped to specific automations

### 3. Key Rotation
- Keys are automatically rotated on failures
- Old keys are immediately invalidated
- Rotation events are logged for audit

### 4. Usage Monitoring
- All key usage is tracked and logged
- Unusual usage patterns trigger alerts
- Cost tracking prevents budget overruns

## 📈 Performance Optimization

### 1. Key Pool Management
- Maintain multiple keys per automation
- Distribute load across available keys
- Prefer keys with lower usage

### 2. Caching
- Cache decrypted keys temporarily
- Avoid repeated decryption operations
- Implement key refresh logic

### 3. Connection Pooling
- Reuse HTTP connections for OpenAI API calls
- Implement connection pooling
- Use async/await for better performance

### 4. Error Handling
- Implement exponential backoff
- Handle rate limits gracefully
- Provide fallback responses

## 🚨 Error Handling

### Common Error Scenarios:

**1. No Available Keys**
```python
if not available_keys:
    return "Service temporarily unavailable - no API keys available"
```

**2. Authentication Errors**
```python
except openai.AuthenticationError:
    # Key is invalid - will be automatically rotated
    logger.warning(f"Authentication error for key {key_id}")
    continue  # Try next key
```

**3. Rate Limit Errors**
```python
except openai.RateLimitError:
    # Rate limit hit - try next key
    logger.warning(f"Rate limit for key {key_id}")
    continue  # Try next key
```

**4. Service Errors**
```python
except openai.APIError as e:
    # Server error - retry with next key
    logger.error(f"API error for key {key_id}: {e}")
    continue  # Try next key
```

## 📊 Monitoring and Alerting

### Key Metrics to Monitor:
- **Key Availability**: Number of active keys per automation
- **Usage Rates**: Tokens per minute/hour per key
- **Error Rates**: Failure rates per key
- **Response Times**: API latency per key
- **Cost Tracking**: Estimated costs per automation

### Alert Conditions:
- **No Available Keys**: Alert when all keys are exhausted
- **High Error Rates**: Alert when error rate > 10%
- **Rate Limit Hits**: Alert when rate limits are frequently hit
- **Cost Thresholds**: Alert when costs exceed budget

## 🎯 Best Practices

### 1. Key Management
- Use platform-managed keys when possible
- Implement proper error handling
- Monitor key health and usage
- Plan for key rotation scenarios

### 2. Performance
- Cache keys appropriately
- Use connection pooling
- Implement retry logic
- Monitor response times

### 3. Security
- Never log API keys
- Use secure key storage
- Implement proper access controls
- Monitor for unusual usage

### 4. Reliability
- Implement fallback mechanisms
- Handle all error scenarios
- Provide graceful degradation
- Monitor service health

## 🔧 Testing

### Test Scenarios:
1. **Normal Operation**: Test with healthy keys
2. **Key Exhaustion**: Test when keys reach limits
3. **Authentication Failures**: Test with invalid keys
4. **Rate Limiting**: Test rate limit handling
5. **Network Failures**: Test network error handling
6. **Key Rotation**: Test automatic key rotation

### Test Implementation:
```python
import pytest
from unittest.mock import Mock, patch

class TestOpenAIIntegration:
    
    @pytest.fixture
    def mock_key_manager(self):
        return Mock()
    
    def test_normal_operation(self, mock_key_manager):
        """Test normal GPT response generation"""
        # Setup mock
        mock_key_manager.select_key.return_value = Mock(id=1)
        mock_key_manager.record_usage.return_value = None
        
        # Test implementation
        # ...
    
    def test_key_exhaustion(self, mock_key_manager):
        """Test behavior when all keys are exhausted"""
        # Setup mock
        mock_key_manager.select_key.return_value = None
        
        # Test implementation
        # ...
    
    def test_authentication_failure(self, mock_key_manager):
        """Test handling of authentication failures"""
        # Setup mock
        mock_key_manager.select_key.return_value = Mock(id=1)
        mock_key_manager.handle_failure.return_value = True
        
        # Test implementation
        # ...
```

## 📞 Support and Troubleshooting

### Common Issues:

**1. "No available keys" error**
- Check if keys are properly configured for the automation
- Verify key status in admin dashboard
- Check if daily limits have been reached

**2. Authentication errors**
- Keys may have been rotated
- Check key validity in OpenAI dashboard
- Verify key permissions

**3. Rate limit errors**
- Too many requests per minute
- Check RPM limits in key configuration
- Consider adding more keys to the pool

**4. High costs**
- Monitor usage patterns
- Implement usage limits
- Consider using cheaper models

### Debugging Steps:
1. Check automation health status
2. Review key usage logs
3. Verify key configuration
4. Test key validity manually
5. Check platform logs for errors

---

**Last Updated:** January 2025  
**Status:** ✅ VERIFIED WITH LIVE TESTING  
**Next Review:** As needed for platform updates
