# 🚀 Zimmer AI Platform

A comprehensive automation management platform with AI-powered features, built with FastAPI, Next.js, and modern web technologies.

## 🌟 Features

### 🤖 **Automation Integration Contract**
- **Secure Service Tokens**: Hash-based authentication for external automation services
- **API Endpoints**: Provision, usage tracking, and KB monitoring
- **Token Rotation**: Admin-controlled service token management
- **Integration Status**: Real-time connection monitoring

### 👨‍💼 **Admin Dashboard**
- **Automation Management**: CRUD operations for automation services
- **Integration Manager**: Service token rotation and URL configuration
- **User Management**: Client oversight and support
- **Knowledge Base**: Template management and monitoring
- **Payment Tracking**: Transaction monitoring and reporting

### 👤 **User Panel**
- **Automation Discovery**: Browse and purchase automation services
- **Dashboard**: Usage statistics and token management
- **Purchase Flow**: Seamless automation acquisition
- **Support System**: Ticket-based customer support

### 🔧 **Technical Features**
- **JWT Authentication**: Secure user and admin authentication
- **Database Support**: PostgreSQL and SQLite compatibility
- **Email Integration**: Password reset and notifications
- **File Upload**: Support ticket attachments
- **RTL Support**: Persian language interface

## 🏗️ Architecture

```
zimmer-full-structure/
├── zimmer-backend/          # FastAPI Backend
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   ├── utils/              # Utilities and helpers
│   └── scripts/            # Database migrations
├── zimmermanagement/        # Admin Dashboard (Next.js)
│   └── zimmer-admin-dashboard/
└── zimmer_user_panel/      # User Panel (Next.js)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite supported)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/zimmer-ai-platform.git
cd zimmer-ai-platform
```

### 2. Backend Setup
```bash
cd zimmer-backend
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env with your configuration
# DATABASE_URL=sqlite:///./zimmer_dashboard.db
# JWT_SECRET_KEY=your-secret-key
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USERNAME=your-email@gmail.com
# EMAIL_PASSWORD=your-app-password

# Run database migration
python scripts/migrate_integration_columns.py

# Start the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Admin Dashboard Setup
```bash
cd zimmermanagement/zimmer-admin-dashboard
npm install

# Copy environment file
cp env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Start the admin dashboard
npm run dev
```

### 4. User Panel Setup
```bash
cd zimmer_user_panel
npm install

# Copy environment file
cp env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start the user panel
npm run dev
```

### 5. Using the Startup Scripts
For Windows:
```powershell
.\start-zimmer.ps1
```

For Linux/Mac:
```bash
./start-zimmer.sh
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=sqlite:///./zimmer_dashboard.db
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

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

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

## 🌐 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Set up reverse proxy (nginx/Apache)
4. Configure SSL certificates
5. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Email**: support@zimmer-ai.com

## 🗺️ Roadmap

- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant architecture
- [ ] API rate limiting
- [ ] Automated testing suite
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Real-time notifications
- [ ] Advanced automation workflows

---

**Built with ❤️ by the Zimmer AI Team**
