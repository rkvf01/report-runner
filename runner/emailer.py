import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email_config: dict, html_body: str) -> None:
    """
    Send the rendered HTML report as an email.

    email_config comes from the YAML file:

    email:
      from: reports@example.com
      to:
        - security@example.com
      cc:
        - cloud@example.com
      subject: "Monthly Cloud Security Posture Report"

    html_body is the final rendered HTML from Jinja.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_host:
        raise ValueError("Missing SMTP_HOST environment variable")

    sender = email_config.get("from")
    recipients = email_config.get("to", [])
    cc = email_config.get("cc", [])
    subject = email_config.get("subject", "Report Runner Report")

    if not sender:
        raise ValueError("Email config is missing required field: from")

    if not recipients:
        raise ValueError("Email config is missing required field: to")

    all_recipients = recipients + cc

    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = ", ".join(recipients)

    if cc:
        message["Cc"] = ", ".join(cc)

    message["Subject"] = subject

    html_part = MIMEText(html_body, "html")
    message.attach(html_part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if smtp_use_tls:
            server.starttls()

        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)

        server.sendmail(sender, all_recipients, message.as_string())