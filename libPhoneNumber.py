import phonenumbers
x = phonenumbers.parse("+442084222233", None)
print x
type(x)
 y = phonenumbers.parse("02084222233", "GB")
 print y
  x == y
  
  z = phonenumbers.parse("+120012301", None)
print z
phonenumbers.is_possible_number(z)
 phonenumbers.is_valid_number(z)
 
 phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
 
