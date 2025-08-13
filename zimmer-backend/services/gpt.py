"""
GPT Service for Zimmer Dashboard
Handles AI response generation with fallback logic
"""

import openai
from typing import Optional
import os
from dotenv import load_dotenv
from models.knowledge import KnowledgeEntry

# Load environment variables
load_dotenv()

# Configure OpenAI (using dummy key for development)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-dummy-key-for-development")

def search_knowledge_base(db, client_id: int, category: str) -> Optional[str]:
    """
    Search the knowledge base for a given client and category.
    Returns the answer if found, else None.
    """
    entry = db.query(KnowledgeEntry).filter(
        KnowledgeEntry.client_id == client_id,
        KnowledgeEntry.category == category
    ).first()
    if entry:
        return entry.answer
    return None

def generate_gpt_response(db, message: str, client_id: int = None, category: str = None) -> Optional[str]:
    """
    Generate GPT response for user message with knowledge base search and fallback logic
    """
    # 1. Try knowledge base if db, client_id, and category are provided
    if db and client_id and category:
        kb_answer = search_knowledge_base(db, client_id, category)
        if kb_answer:
            return kb_answer
    
    # Fallback rules - check for complex keywords
    complex_keywords = ["complex", "technical", "specific", "detailed", "custom"]
    message_lower = message.lower()
    has_complex_keywords = any(keyword in message_lower for keyword in complex_keywords)
    word_count = len(message.split())
    is_too_long = word_count > 20
    if has_complex_keywords or is_too_long:
        return None
    
    # GPT call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for Zimmer, a travel and visa services company. Provide clear, concise, and helpful responses to customer inquiries. Keep responses friendly and professional."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        print(f"GPT API error: {str(e)}")
        if "Incorrect API key" in str(e):
            return f"Hello! I'm Zimmer's AI assistant. I'd be happy to help you with {message.lower()}. Please contact our support team for more detailed assistance."
        return None

def count_tokens(text: str) -> int:
    """
    Estimate token count for text (simplified implementation)
    
    Args:
        text (str): Text to count tokens for
        
    Returns:
        int: Estimated token count
    """
    # Simple estimation: 1 token ≈ 4 characters for English text
    return len(text) // 4

def get_response_cost(tokens_used: int) -> float:
    """
    Calculate cost for GPT-4 response
    
    Args:
        tokens_used (int): Number of tokens used
        
    Returns:
        float: Cost in USD
    """
    # GPT-4 pricing (approximate)
    # Input: $0.03 per 1K tokens
    # Output: $0.06 per 1K tokens
    # For simplicity, we'll use average cost
    cost_per_token = 0.000045  # Average of input/output cost
    return tokens_used * cost_per_token 