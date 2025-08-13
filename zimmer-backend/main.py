from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Zimmer Internal Management Dashboard",
    description="Backend API for Zimmer's internal management and automation tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3001", 
        "http://zimmerai.com"
    ],  # Configure specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS test successful", "timestamp": "2025-07-07"}

# Import and include routers
from routers import users, admin, fallback, knowledge, telegram, ticket, ticket_message
app.include_router(users.router, prefix="/api", tags=["users"])
from routers.admin import router as admin_router
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(fallback.router, prefix="/api/admin", tags=["fallback"])
app.include_router(knowledge.router, prefix="/api", tags=["knowledge"])
app.include_router(ticket.router, prefix="/api", tags=["tickets"])
app.include_router(ticket_message.router, prefix="/api", tags=["ticket-messages"])
app.include_router(telegram.router)
from routers.password_reset import router as password_reset_router
app.include_router(password_reset_router, prefix="/api", tags=["password-reset"])
from routers.admin.automation import router as admin_automation_router
app.include_router(admin_automation_router, prefix="/api/admin", tags=["automation"])
from routers.admin.kb_monitoring import router as kb_monitoring_router
app.include_router(kb_monitoring_router, prefix="/api/admin", tags=["kb-monitoring"])
from routers.admin.kb_monitoring_simple import router as kb_monitoring_simple_router
app.include_router(kb_monitoring_simple_router, prefix="/api/admin", tags=["kb-monitoring-simple"])
from routers.admin.kb_history import router as kb_history_router
app.include_router(kb_history_router, prefix="/api/admin", tags=["kb-history"])
from routers.admin.backups import router as backups_router
app.include_router(backups_router, prefix="/api/admin", tags=["backups"])
from routers.admin.kb_templates import router as kb_templates_router
app.include_router(kb_templates_router, prefix="/api/admin", tags=["kb-templates"])
from routers.admin.automation_integrations import router as automation_integrations_router
app.include_router(automation_integrations_router, prefix="/api/admin", tags=["automation-integrations"])
from routers.automations import router as automations_router
app.include_router(automations_router, prefix="/api", tags=["automations"])
from routers.automation_usage import router as automation_usage_router
app.include_router(automation_usage_router, prefix="/api", tags=["automation-usage"])

# Import all models to ensure they're registered with Base
from models import *

# Create all tables (development mode only) - after all models are imported
Base.metadata.create_all(bind=engine)

# Start backup scheduler
from scheduler import backup_scheduler
backup_scheduler.start()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Zimmer Internal Management Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "zimmer-dashboard"}



@app.post("/dev/seed")
async def seed_data():
    """Development endpoint to seed sample data"""
    try:
        from utils.seeder import seed_sample_data
        seed_sample_data()
        return {"message": "Sample data seeded successfully"}
    except Exception as e:
        return {"error": f"Failed to seed data: {str(e)}"}

@app.post("/dev/test-gpt")
async def test_gpt(message: str):
    """Development endpoint to test GPT service"""
    try:
        from services.gpt import generate_gpt_response, count_tokens, get_response_cost
        
        # Generate response
        response = generate_gpt_response(message)
        
        if response is None:
            return {
                "message": "Fallback triggered",
                "reason": "Complex keywords or long message detected",
                "input_message": message,
                "word_count": len(message.split())
            }
        else:
            tokens = count_tokens(response)
            cost = get_response_cost(tokens)
            return {
                "message": "GPT response generated",
                "response": response,
                "tokens_used": tokens,
                "estimated_cost": f"${cost:.4f}",
                "input_message": message,
                "word_count": len(message.split())
            }
    except Exception as e:
        return {"error": f"GPT test failed: {str(e)}"} 