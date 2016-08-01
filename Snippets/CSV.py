import csv

#writing csv file
c = csv.writer(open("MYFILE.csv", "wb"))
c.writerow(["Name","Address","Telephone","Fax","E-mail","Others"])

#reading csv file
cr = csv.reader(open("MYFILE.csv","rb"))
for row in cr:    
    print row
    
for row in reader:    
    print row[2], row[-2]
