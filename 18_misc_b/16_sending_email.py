import email
import smtplib
import socketserver
import threading
from email import policy
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid, parseaddr

# To keep this lesson offline, a tiny FAKE SMTP server runs inside the script.
# It speaks just enough SMTP to receive a message, and keeps the messages it gets.
received = []


class FakeSmtpHandler(socketserver.StreamRequestHandler):
    def reply(self, text):
        self.wfile.write(text.encode() + b"\r\n")

    def handle(self):
        mail_from, recipients = None, []
        self.reply("220 fake.local ready")
        while True:
            line = self.rfile.readline()
            if not line:
                break
            command = line.decode("ascii", "replace").strip()
            upper = command.upper()
            if upper.startswith(("EHLO", "HELO")):
                self.reply("250 fake.local")
            elif upper.startswith("MAIL FROM:"):
                mail_from = command[10:].strip().strip("<>")
                self.reply("250 OK")
            elif upper.startswith("RCPT TO:"):
                recipients.append(command[8:].strip().strip("<>"))
                self.reply("250 OK")
            elif upper == "DATA":
                self.reply("354 End data with <CR><LF>.<CR><LF>")
                chunks = []
                while True:
                    row = self.rfile.readline()
                    if row.rstrip(b"\r\n") == b".":
                        break
                    chunks.append(row)
                received.append({"from": mail_from, "to": recipients, "data": b"".join(chunks)})
                self.reply("250 OK queued")
            elif upper == "QUIT":
                self.reply("221 Bye")
                break
            else:
                self.reply("502 command not implemented")


server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), FakeSmtpHandler)
server.daemon_threads = True
threading.Thread(target=server.serve_forever, daemon=True).start()
port = server.server_address[1]


def send(message):
    """Send with smtplib, then return the message as the 'server' received it."""
    with smtplib.SMTP("127.0.0.1", port, local_hostname="localhost", timeout=5) as smtp:
        smtp.send_message(message)
    return email.message_from_bytes(received[-1]["data"], policy=policy.default)


# 1. A simple message
msg = EmailMessage()
msg["From"] = formataddr(("Alice", "alice@example.com"))
msg["To"] = "bob@example.com, carol@example.com"
msg["Subject"] = "Report"
msg.set_content("Hello Bob")

parsed = send(msg)
print(received[0]["from"], received[0]["to"])   # alice@example.com ['bob@example.com', 'carol@example.com']
print(parsed["Subject"], parsed["From"])        # Report Alice <alice@example.com>
print(parsed.get_content().strip())             # Hello Bob

# 2. An attachment
msg = EmailMessage()
msg["From"], msg["To"], msg["Subject"] = "alice@example.com", "bob@example.com", "File"
msg.set_content("See attached")
msg.add_attachment(b"\x01\x02", maintype="application", subtype="octet-stream", filename="data.bin")
parsed = send(msg)
attachments = list(parsed.iter_attachments())
print([a.get_filename() for a in attachments], attachments[0].get_content())    # ['data.bin'] b'\x01\x02'

# 3. Plain text AND HTML in one message
msg = EmailMessage()
msg["From"], msg["To"], msg["Subject"] = "alice@example.com", "bob@example.com", "News"
msg.set_content("Plain text")
msg.add_alternative("<p>Hello</p>", subtype="html")
parsed = send(msg)
print(parsed.get_body(preferencelist=("html", "plain")).get_content_type(), parsed.is_multipart())
# text/html True
print([part.get_content_type() for part in parsed.walk()])
# ['multipart/alternative', 'text/plain', 'text/html']

# 4. Non-ASCII text in the body and in the subject
msg = EmailMessage()
msg["From"], msg["To"], msg["Subject"] = "alice@example.com", "bob@example.com", "Café"
msg.set_content("héllo", cte="quoted-printable")
parsed = send(msg)
print(parsed.get_content().strip(), parsed["Subject"])      # héllo Café

# 5. Helpers for addresses and headers
print(parseaddr("Ann <ann@example.com>"), formataddr(("Ann", "ann@example.com")))
# ('Ann', 'ann@example.com') Ann <ann@example.com>
print(formatdate(0, usegmt=True), make_msgid(domain="example.com").endswith("@example.com>"))
# Thu, 01 Jan 1970 00:00:00 GMT True

print(len(received))                            # 4
server.shutdown()
server.server_close()

# SENDING REAL E-MAIL
#   import os, smtplib
#   with smtplib.SMTP("smtp.example.com", 587) as smtp:          # 587: start plain, then upgrade
#       smtp.starttls()                                          # encrypt the connection
#       smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
#       smtp.send_message(msg)
#   or  smtplib.SMTP_SSL("smtp.example.com", 465)                # encrypted from the first byte
# RULES
#   - Never write passwords in the code or commit them: use environment variables or a secrets store.
#   - Gmail and others need an "app password" or OAuth, not your normal password.
#   - Providers limit how many messages you can send; for many messages use a service with an API
#     (SendGrid, Mailgun, Amazon SES). Without SPF/DKIM set up on your domain, mail lands in spam.
#   - Reading mail: imaplib (IMAP) and poplib (POP3) in the standard library.
#   - Validate addresses you get from users, and never put user text into the headers unchecked
#     (header injection): EmailMessage rejects line breaks in headers.