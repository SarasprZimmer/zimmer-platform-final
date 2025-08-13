# Import all models to ensure they're registered with SQLAlchemy Base
# Import order matters for relationships

# First, import models without relationships
from .user import User
from .automation import Automation
from .user_automation import UserAutomation
from .payment import Payment
from .fallback_log import FallbackLog
from .token_usage import TokenUsage
from .knowledge import KnowledgeEntry
from .kb_template import KBTemplate
from .ticket import Ticket
from .ticket_message import TicketMessage
from .password_reset_token import PasswordResetToken
from .kb_status_history import KBStatusHistory
from .backup import BackupLog

# Export all models
__all__ = [
    'User',
    'Automation', 
    'UserAutomation',
    'Payment',
    'FallbackLog',
    'TokenUsage',
    'KnowledgeEntry',
    'KBTemplate',
    'Ticket',
    'TicketMessage',
    'PasswordResetToken',
    'KBStatusHistory',
    'BackupLog'
] 