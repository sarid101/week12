# Lab Week 12: Automating Communications (Email & SMS)

SP352301 Script Programming — ภาคเรียน 1/2569

โปรเจกต์นี้ใช้ Python ส่งอีเมลผ่าน **SMTP** (`smtplib` + `email.mime`) รับและอ่านอีเมลผ่าน **IMAP** (`imaplib` + `email`) และส่ง SMS ผ่าน **email-to-SMS gateway** โดยเก็บรหัสผ่านไว้ในไฟล์ `.env` (ไม่ hardcode ในโค้ด)

## Key Concepts Demonstrated

* **SMTP** — เชื่อมต่อ `smtp.gmail.com:587`, `starttls()`, `login()` ด้วย App Password, `send_message()`
* **MIME** — `MIMEMultipart` รวมเนื้อหา + ไฟล์แนบ, `MIMEText` (utf-8 รองรับภาษาไทย), `MIMEApplication` สำหรับ PDF
* **IMAP** — `IMAP4_SSL`, `select('INBOX')`, ค้นหาด้วย `UNSEEN` + `FROM` + `SUBJECT`, ดึงเนื้อหา, ดาวน์โหลดไฟล์แนบ, ตั้งค่า `\Seen`
* **Email Parsing** — `msg.walk()` แยกส่วน text/plain กับ attachment, `decode_header()` ถอดรหัสหัวเรื่องภาษาไทย
* **SMS Gateway** — ส่งอีเมลไปที่ `เบอร์@txt.att.net` เพื่อแปลงเป็น SMS
* **Secure Credentials** — `python-dotenv` โหลดค่าจาก `.env` ซึ่งอยู่ใน `.gitignore`

## Setup & How to Run

```bash
git clone https://github.com/sarid101/email-sms-automator.git
cd email-sms-automator
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install python-dotenv reportlab
copy .env.example .env          # macOS/Linux: cp .env.example .env
```

แก้ไฟล์ `.env` ใส่ค่าของตัวเอง:

```ini
SENDER_EMAIL=your_email@gmail.com
SENDER_APP_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
IMAP_SERVER=imap.gmail.com
TEST_RECIPIENT_EMAIL=your_email@gmail.com
TEST_SMS_PHONE_NUMBER=1234567890
TEST_SMS_CARRIER=att
STUDENT_NAME=สาริษฐ์ บุตรช่วง
STUDENT_ID=663380365-3
```

แล้วรัน:

```bash
python main.py
```

### การสร้าง Gmail App Password

1. เปิด **2-Step Verification** ที่ <https://myaccount.google.com/security>
2. ไปที่ <https://myaccount.google.com/apppasswords> สร้างรหัสใหม่ (ตั้งชื่อเช่น `python-lab`)
3. คัดลอกรหัส 16 ตัวอักษรใส่ `SENDER_APP_PASSWORD` (ใส่แบบมีช่องว่างก็ได้ โปรแกรมจะตัดช่องว่างให้)

รหัสผ่าน Gmail ปกติใช้กับ SMTP/IMAP ไม่ได้ ต้องใช้ App Password เท่านั้น

## สิ่งที่โปรแกรมทำ

| Task | การทำงาน | หัวเรื่องอีเมล |
| --- | --- | --- |
| 1 | ส่งอีเมลข้อความธรรมดา | `ทดสอบ Automated Python Test Email` |
| 2 | ส่งอีเมลพร้อมไฟล์แนบ `dummy_report.pdf` | `ทดสอบ Python Test Email with Attachment - Daily Report` |
| 3 | ส่ง SMS ผ่าน gateway `@txt.att.net` | (ไม่มีหัวเรื่อง) |
| 4 | ส่งอีเมลหาตัวเอง → ค้นหาอีเมลที่ยังไม่อ่าน → แสดงผู้ส่ง/หัวเรื่อง/เนื้อหา → ดาวน์โหลดไฟล์แนบลง `data/attachments/` → ตั้งเป็นอ่านแล้ว | `ทดสอบ Python Test: Email for Receiving Demo` |

ทุกอีเมลขึ้นต้นเนื้อหาด้วย `STUDENT_NAME STUDENT_ID` จึงเห็นชื่อและรหัสนักศึกษาในหน้า Inbox ตามที่ Lab กำหนด

**เรื่อง Task 3 (SMS):** gateway แบบ `@txt.att.net` ใช้ได้เฉพาะเครือข่ายในอเมริกา เครือข่ายไทย (AIS, True, dtac) ไม่มีบริการนี้ Gmail จึงตีกลับด้วยข้อความ "ไม่พบที่อยู่ … txt.att.net" เป็นเรื่องปกติ (ในภาพตัวอย่างของอาจารย์ก็มีอีเมลตีกลับนี้) ถ้าต้องการส่ง SMS จริงต้องใช้บริการ API เช่น Twilio

## Screenshot

ให้แคปหน้า Gmail Inbox หลังรัน `python main.py` แล้วบันทึกเป็น `screenshots/gmail_inbox.png`

![Gmail inbox](screenshots/gmail_inbox.png)

## Project Structure

```
email-sms-automator/
├── src/
│   ├── __init__.py          # Python package marker
│   ├── email_sender.py      # ส่งอีเมล (SMTP)
│   ├── email_receiver.py    # รับ/อ่านอีเมล (IMAP)
│   ├── sms_gateway.py       # ส่ง SMS ผ่าน email gateway
│   └── utils.py             # Logging, โหลด .env, สร้างโฟลเดอร์
├── data/
│   ├── attachments/         # ไฟล์แนบที่ดาวน์โหลดมา (อยู่ใน .gitignore)
│   └── dummy_report.pdf     # ไฟล์แนบตัวอย่าง
├── screenshots/
│   └── gmail_inbox.png      # ภาพ Inbox หลังรันโปรแกรม
├── .env.example             # ตัวอย่างไฟล์ตั้งค่า (คัดลอกเป็น .env)
├── create_dummy_report.py   # สร้าง dummy_report.pdf ใหม่
├── main.py                  # จุดเริ่มต้นโปรแกรม
├── lab_week12_colab.ipynb   # Notebook สำหรับรันบน Google Colab
├── .gitignore
└── README.md
```

## หมายเหตุการแก้โค้ดจากต้นฉบับ

* **`.gitignore` (สำคัญ):** ต้นฉบับเขียน `.env  # DO NOT COMMIT YOUR .env FILE` ไว้บรรทัดเดียวกัน แต่ `.gitignore` ไม่รองรับคอมเมนต์ท้ายบรรทัด Git จึงตีความทั้งบรรทัดเป็นชื่อไฟล์ และ **ไม่ ignore `.env` จริง** ซึ่งอาจทำให้ App Password หลุดขึ้น GitHub ผมแยกคอมเมนต์ไว้คนละบรรทัดแล้ว
* **Import:** เปลี่ยน `from .utils` / `from .email_sender` เป็น `from utils` / `from email_sender` เพราะ `main.py` เพิ่ม `src` เข้า `sys.path` (relative import จะ error)
* **IMAP UID:** ต้นฉบับใช้ `search()`/`fetch()` ซึ่งคืน *sequence number* ที่เปลี่ยนได้ แล้วยังปิด-เปิดการเชื่อมต่อใหม่ก่อน fetch ผมเปลี่ยนเป็น `mail.uid('search'|'fetch'|'store', ...)` ซึ่งเป็น UID ถาวรตามที่ชื่อตัวแปรตั้งใจไว้
* **`BODY.PEEK[]`:** ใช้แทน `RFC822` เพื่อไม่ให้อีเมลถูกตั้งเป็นอ่านแล้วทันทีที่ดึง ทำให้พารามิเตอร์ `mark_as_read=False` ใช้ได้จริง
* **ภาษาไทย:** `MIMEText(..., 'utf-8')` และถอดรหัสชื่อไฟล์แนบด้วย `decode_header`
* **`.env` path:** โหลดจากโฟลเดอร์โปรเจกต์เสมอ ไม่ขึ้นกับโฟลเดอร์ที่รัน และตัดช่องว่างใน App Password ให้อัตโนมัติ
* ถ้าไม่มี `dummy_report.pdf` Task 4 จะยังส่งอีเมลได้ (ต้นฉบับจะ log error)

## Debugging

* **`Environment variable '...' not set`** — ยังไม่ได้สร้าง `.env` หรือสะกดชื่อตัวแปรผิด
* **`SMTPAuthenticationError` / `IMAP authentication failed`** — ใช้รหัส Gmail ปกติแทน App Password หรือยังไม่เปิด 2-Step Verification
* **`No matching unread emails found`** — อีเมลอาจมาช้า ให้เพิ่ม `time.sleep()` ใน Task 4 หรือมีอีเมลหัวเรื่องเดียวกันที่อ่านไปแล้ว
* **SMS ไม่ถึง / อีเมลตีกลับ** — ปกติสำหรับเบอร์ไทย (ดูหมายเหตุ Task 3)
* **Connection timed out** — เครือข่ายมหาวิทยาลัยอาจบล็อกพอร์ต 587/993 ลองใช้ hotspot มือถือ
