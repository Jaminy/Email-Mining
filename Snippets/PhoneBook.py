phonebook = {
	"xxx" : 111222333,
	"yyy" : 333444555,
	"zzz" : 444555666

}


for name, number in phonebook.iteritems():
    print "Phone number of %s is %d" % (name, number)
