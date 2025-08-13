# 🚀 Zimmer Backend API

A FastAPI-based backend for the Zimmer automation management platform with AI-powered features and secure automation integration contracts.

## 🌟 Features

### 🤖 **Automation Integration Contract**
- **Secure Service Tokens**: Hash-based authentication using bcrypt
- **API Endpoints**: Provision, usage tracking, and KB monitoring
- **Token Rotation**: Admin-controlled service token management
- **Integration Status**: Real-time connection monitoring

### 🔐 **Security & Authentication**
- **JWT Authentication**: Secure token-based authentication
- **Role-based Access**: Admin and user role management
- **Input Validation**: Pydantic schema validation
- **CORS Protection**: Cross-origin request handling

### 📊 **Core Functionality**
- **User Management**: Registration, authentication, profile management
- **Automation Management**: CRUD operations for automation services
- **Payment Processing**: Transaction tracking and management
- **Support System**: Ticket-based customer support
- **Knowledge Base**: Template management and monitoring

## 🏗️ Architecture

```
zimmer-backend/
├── models/                 # SQLAlchemy database models
│   ├── user.py            # User authentication and profiles
│   ├── automation.py      # Automation service definitions
│   ├── user_automation.py # User-automation relationships
│   └── ...
├── routers/               # FastAPI route handlers
│   ├── admin/            # Admin-only endpoints
│   ├── users.py          # User management
│   ├── automations.py    # Automation operations
│   └── ...
├── services/             # Business logic layer
│   ├── email_service.py  # Email notifications
│   ├── token_manager.py  # Token usage tracking
│   └── ...
├── utils/                # Utilities and helpers
│   ├── auth.py          # Authentication utilities
│   ├── service_tokens.py # Service token management
│   └── ...
└── scripts/              # Database migrations
    └── migrate_integration_columns.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite supported)

### Installation

1. **Clone and Setup**
```bash
cd zimmer-backend
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp env.example .env
# Edit .env with your configuration
```

3. **Database Setup**
```bash
# Run migration to add integration columns
python scripts/migrate_integration_columns.py
```

4. **Start the Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

```env
# Database
DATABASE_URL=sqlite:///./zimmer_dashboard.db

# JWT Authentication
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Automation Service Tokens
AUTOMATION_1_SERVICE_TOKEN=your-service-token
AUTOMATION_2_SERVICE_TOKEN=your-service-token
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh

#### Admin Endpoints
- `POST /api/admin/automations/{automation_id}/rotate-token` - Rotate service token
- `GET /api/admin/automations/{automation_id}/integration` - Get integration details
- `GET /api/admin/automations` - List all automations
- `POST /api/admin/automations` - Create automation
- `PUT /api/admin/automations/{id}` - Update automation
- `DELETE /api/admin/automations/{id}` - Delete automation

#### User Endpoints
- `POST /api/automations/{automation_id}/provision` - Provision automation
- `POST /api/automation-usage/consume` - Report usage
- `GET /api/user/automations` - User's automations
- `GET /api/automations/available` - Available automations

#### Support System
- `GET /api/tickets` - List user tickets
- `POST /api/tickets` - Create support ticket
- `GET /api/tickets/{ticket_id}` - Get ticket details
- `POST /api/tickets/{ticket_id}/messages` - Add ticket message

## 🗄️ Database Schema

### Core Tables
- **users**: User accounts and authentication
- **automations**: Automation service definitions
- **user_automations**: User-automation relationships
- **tokens**: Token usage tracking
- **tickets**: Support ticket system
- **payments**: Payment transactions

### Integration Tables
- **automations**: Extended with integration URLs and service tokens
- **user_automations**: Extended with provisioning status and timestamps

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Service Token Hashing**: bcrypt-hashed service tokens
- **Input Validation**: Pydantic schema validation
- **CORS Protection**: Cross-origin request handling
- **Rate Limiting**: API request throttling

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_auth.py

# Run with coverage
python -m pytest --cov=app tests/
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t zimmer-backend .

# Run container
docker run -p 8000:8000 zimmer-backend

# Using Docker Compose
docker-compose up -d
```

## 🔧 Development

### Code Style
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Database Migrations
```bash
# Run migration script
python scripts/migrate_integration_columns.py
```

### Adding New Endpoints
1. Create route handler in `routers/`
2. Add Pydantic schemas in `schemas/`
3. Update database models if needed
4. Add tests
5. Update documentation

## 🚀 Production Deployment

### Manual Deployment
1. Set up production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Set up reverse proxy (nginx/Apache)
4. Configure SSL certificates
5. Set up monitoring and logging

### Docker Deployment
```bash
# Production build
docker build -t zimmer-backend:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:port/db \
  -e JWT_SECRET_KEY=your-secret \
  zimmer-backend:latest
```

## 📊 Monitoring

### Health Check
- `GET /health` - Basic health check
- `GET /docs` - API documentation

### Logging
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ by the Zimmer AI Team** 