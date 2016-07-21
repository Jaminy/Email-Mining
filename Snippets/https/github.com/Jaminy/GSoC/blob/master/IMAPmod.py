import sys
import imaplib
import getpass
import email

M = imaplib.IMAP4_SSL('imap.gmail.com')


import getpass
import sys

###### read command line, password
if len(sys.argv) < 1:
    print "please specify username/email address"
    exit ()

username = sys.argv[1]

print "Type your password:"
password = getpass.getpass()


print "Type your password:"
password = getpass.getpass()


