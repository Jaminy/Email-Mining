import hashlib
email = 'jaminy02@gmail.com'.encode('utf-8')
hash = hashlib.md5(email.strip().lower()).hexdigest()
