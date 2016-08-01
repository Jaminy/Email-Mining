>>> y=re.findall(r'\d+', 'hello +94716772265')
>>> y
['94716772265']
>>> print y
['94716772265']
>>> z=phonenumbers.parse("+" + y[0])
>>> print z
Country Code: 94 National Number: 716772265
>>> z=phonenumbers.parse("+", "US")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build/bdist.linux-x86_64/egg/phonenumbers/phonenumberutil.py", line 2576, in parse
phonenumbers.phonenumberutil.NumberParseException: (1) The string supplied did not seem to be a phone number.
>>> z
PhoneNumber(country_code=94, national_number=716772265, extension=None, italian_leading_zero=None, number_of_leading_zeros=None, country_code_source=None, preferred_domestic_carrier_code=None)
>>> phonenumbers.is_possible_number(z)
True
>>> phonenumbers.is_valid_number(z)
True
