import imaplib
import email
import getpass

mail = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    mail.login('jaminy1234@gmail.com', getpass.getpass())
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "

rv, mailboxes = mail.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes
mail.list() #Lists the folders in the gmail
mail.select("inbox") # connect to inbox.

result, data = mail.uid('search', None, "ALL")  # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

from email.parser import Parser
parser = Parser()

emailText = raw_email
email = parser.parsestr(emailText)

print email.get('From')
print email.get('To')
print email.get('Subject')

'''if email.is_multipart():
    for part in email.get_payload():
        print part.get_payload()
else:
    print email.get_payload()
'''
exml =lxml.html.fromstring(text)
exml.test_content()
email.logout
