from settings import settings
import emails

def send_email(to: str, subject: str, html: str):
    if not settings.SMTP_HOST:
        # dev/mock: print to console
        print(f"[DEV EMAIL] To:{to} Subject:{subject}\n{html}")
        return True
    m = emails.Message(subject=subject, html=html, mail_from=settings.SMTP_FROM)
    r = m.send(
        to=to,
        smtp={
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "user": settings.SMTP_USER,
            "password": settings.SMTP_PASSWORD,
            "tls": True,
        },
    )
    return r.status_code == 250
