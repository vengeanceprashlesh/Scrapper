import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS")

        if not self.user or not self.password:
            raise ValueError("EMAIL_USER or EMAIL_PASS environment variables are not set.")

    def send_report(self, recipient: str, analysis_data: Dict):
        """
        Sends an HTML email with the stock analysis report.
        """
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = recipient
        msg['Subject'] = f"Daily Stock Report: {analysis_data['ticker']}"

        body = f"""
        <html>
        <body>
            <h2>Daily Stock Report for {analysis_data['ticker']}</h2>
            <p><strong>Price:</strong> ${analysis_data['last_close']}</p>
            <p><strong>Change:</strong> {analysis_data['change_percent']}%</p>
            <hr>
            <h3>AI Analysis</h3>
            <p>{analysis_data['analysis']}</p>
            <hr>
            <h3>Top Headlines</h3>
            <ul>
                {''.join([f'<li>{h}</li>' for h in analysis_data['headlines']])}
            </ul>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, recipient, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {recipient}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise
