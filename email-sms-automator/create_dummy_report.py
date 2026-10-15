# email-sms-automator/create_dummy_report.py
# Helper script: creates data/dummy_report.pdf used as the email attachment.
# Requires: pip install reportlab
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "dummy_report.pdf")
os.makedirs(os.path.dirname(path), exist_ok=True)

c = canvas.Canvas(path, pagesize=A4)
_, height = A4
c.setFont("Helvetica-Bold", 18)
c.drawString(72, height - 80, "Daily Report")
c.setFont("Helvetica", 11)
lines = [
    f"Generated: {datetime.date.today().isoformat()}",
    "",
    "This is a dummy report used to demonstrate sending",
    "email attachments with Python (smtplib + email.mime).",
    "",
    "Orders processed: 42",
    "Emails sent: 4",
    "Status: OK",
]
y = height - 115
for line in lines:
    c.drawString(72, y, line)
    y -= 18
c.showPage()
c.save()
print(f"Created: {path}")
