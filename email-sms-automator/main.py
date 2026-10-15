# email-sms-automator/main.py
import sys
import os
import time

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from email_sender import EmailSender
from email_receiver import EmailReceiver
from sms_gateway import SMSGateway
from utils import setup_logging, get_env_variable, ensure_directory_exists

logger = setup_logging(__name__)

SUBJECT_PREFIX = "ทดสอบ"  # Subject prefix required by the lab
RECEIVE_SUBJECT = "Python Test: Email for Receiving Demo"


def main():
    """
    Main function to orchestrate email and SMS automation tasks.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    attachments_dir = os.path.join(data_dir, 'attachments')
    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    # --- Load Credentials from Environment Variables ---
    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD").replace(" ", "")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")

        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")

        student_name = get_env_variable("STUDENT_NAME")
        student_id = get_env_variable("STUDENT_ID")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}. Please set all required environment variables in your .env file.")
        sys.exit(1)

    # Student signature placed at the start of every email body
    signature = f"{student_name} {student_id}"

    # --- Initialize Handlers ---
    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_app_password)
    email_receiver = EmailReceiver(imap_server, sender_email, sender_app_password)
    sms_gateway = SMSGateway(email_sender)

    attachment_file_path = os.path.join(data_dir, 'dummy_report.pdf')

    # --- Task 1: Send a simple plaintext email ---
    logger.info("--- Task 1: Sending a simple plaintext email ---")
    email_sender.send_email(
        recipient_email=test_recipient_email,
        subject=f"{SUBJECT_PREFIX} Automated Python Test Email",
        body=f"{signature}\n\nHello from your Python automation script! This is a plain text email."
    )
    time.sleep(2)  # Give a short delay

    # --- Task 2: Send an email with an attachment ---
    logger.info("--- Task 2: Sending an email with an attachment ---")
    if os.path.exists(attachment_file_path):
        email_sender.send_email(
            recipient_email=test_recipient_email,
            subject=f"{SUBJECT_PREFIX} Python Test Email with Attachment - Daily Report",
            body=f"{signature}\n\nPlease find the daily report attached.",
            attachment_path=attachment_file_path
        )
    else:
        logger.warning(f"Attachment file not found at '{attachment_file_path}'. Skipping attachment email.")
    time.sleep(2)  # Give a short delay

    # --- Task 3: Send an SMS via email gateway ---
    logger.info("--- Task 3: Sending an SMS via email gateway ---")
    sms_message = f"{signature} - Hello from Python! This is an automated SMS via email gateway."
    sms_gateway.send_sms(
        phone_number=test_sms_phone_number,
        message=sms_message,
        carrier_name=test_sms_carrier
    )
    time.sleep(5)  # Give more time for SMS to arrive

    # --- Task 4: Receive and process emails ---
    logger.info("--- Task 4: Receiving and processing emails ---")
    # Send a new email to self to ensure there's an email to find for demo
    email_sender.send_email(
        recipient_email=sender_email,  # Send to self
        subject=f"{SUBJECT_PREFIX} {RECEIVE_SUBJECT}",
        body=f"{signature}\n\nThis email is specifically for the receiving demo. It has an attachment!",
        attachment_path=attachment_file_path if os.path.exists(attachment_file_path) else None
    )
    logger.info("Sent a demo email to self for receiving task. Waiting a few seconds...")
    time.sleep(10)  # Give email server time to process and deliver

    # Search for unseen emails from self with a specific subject
    uids = email_receiver.search_emails(
        criteria='UNSEEN',
        from_sender=sender_email,
        subject_contains=RECEIVE_SUBJECT
    )

    if uids:
        logger.info(f"Found {len(uids)} matching unread email(s) for receiving demo.")
        for uid in uids:
            logger.info(f"Processing email UID: {uid.decode('utf-8')}")
            email_details = email_receiver.fetch_email_content(
                uid=uid,
                mark_as_read=True,
                download_attachments_dir=attachments_dir
            )
            if email_details:
                logger.info(f"  Sender: {email_details['sender']}")
                logger.info(f"  Subject: {email_details['subject']}")
                logger.info(f"  Body Snippet: {email_details['body_snippet']}")
                if email_details['attachments_downloaded']:
                    logger.info(f"  Attachments downloaded: {', '.join(email_details['attachments_downloaded'])}")
                else:
                    logger.info("  No attachments downloaded for this email.")
            else:
                logger.error(f"Could not retrieve details for email UID: {uid.decode('utf-8')}")
    else:
        logger.info("No matching unread emails found for receiving demo.")

    logger.info("--- All communication automation tasks completed ---")


if __name__ == "__main__":
    main()
