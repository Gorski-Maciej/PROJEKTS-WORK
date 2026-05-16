from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


async def send_email(to: str, subject: str, body: str) -> bool:
    host = os.getenv('SMTP_HOST')
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    from_addr = os.getenv('EMAIL_FROM', user or 'infraflow@example.com')
    port = int(os.getenv('SMTP_PORT', '587'))

    if not host or not user or not password:
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP(host, port, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(msg)
    return True
