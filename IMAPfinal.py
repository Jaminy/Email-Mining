import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('username@gmail.com', 'password')
mail.list() #Lists the folders in the gmail
mail.select("inbox") # connect to inbox.

result, data = mail.uid('search', None, "ALL")  # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

import email
email_message = email.message_from_string(raw_email)
 
print email_message['To']
print email_message['CC']
 
print email.utils.parseaddr(email_message['From']) 
 
print email_message.items()

if email.is_multipart():
    for part in email.get_payload():
        print part.get_payload()
else:
    print email.get_payload()
