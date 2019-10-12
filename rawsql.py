import sqlite3
import csv

con = sqlite3.connect('app.db')
outfile = open('mydump.csv', 'wb')
outcsv = csv.writer(outfile)

cursor = con.execute('select * from User')

# dump column titles (optional)
outcsv.writerow(x[0] for x in cursor.description)
# dump rows
outcsv.writerows(cursor.fetchall())

outfile.close()