import imaplib
import email
import getpass
from email.parser import Parser
from email.utils import parseaddr
from flask import Flask, jsonify, render_template
import logging
from hashlib import md5

##### Set up some global data structures

contacts = {}

##### Perform mining

mail = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    mail.login('jaminy1234@gmail.com', getpass.getpass())
except imaplib.IMAP4.error:
    logging.error("LOGIN FAILED!!!")

rv, mailboxes = mail.list()

if rv == 'OK':
    logging.debug("Discovered Mailboxes: %r", mailboxes)

mail.select("INBOX") # connect to inbox.

result, data = mail.uid('search', None, "ALL")  # search and return uids
uids = data[0].split()

for uid in uids:
    result, data = mail.uid('fetch', uid, '(RFC822)')
    raw_email = data[0][1]

    parser = Parser()

    emailText = raw_email
    email = parser.parsestr(emailText)

    sender_realname, sender = parseaddr(email.get('From'))

    if sender not in contacts.keys():
        contacts[sender] = {}
        contacts[sender]['email'] = sender
        contacts[sender]['realname'] = sender_realname
        contacts[sender]['gravatar'] = "https://www.gravatar.com/avatar/" + md5(sender.strip().lower()).hexdigest()
        contacts[sender]['mails'] = []

    contacts[sender]['mails'].append((email.get('Subject'), email.get('Date')))

##### Web Frontend

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", contacts=contacts)

@app.route("/contact/<contact>")
def contact(contact):
    return render_template("contact.html", c=contacts[contact])

if __name__ == "__main__":
        app.run(debug=True)
