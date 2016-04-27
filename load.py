#!/usr/bin/python

import getpass
import pg8000
import csv

def insertDict(d, cursor):
  if 'dasf' in d:
    del d['dasf']
  cols = ','.join(d.keys())
  reps = ','.join([ '(%s)' for x in d.keys() ])
  vals = tuple(d.values())
  stmt = "INSERT INTO weather (%s) VALUES (%s);" % (cols, reps)
  cursor.execute(stmt, vals)

def loadFile(fname, cursor):
  print 'loading: ' + fname
  with open(fname) as f:
    csvread = csv.reader(f)
    headers = []
    for row in csvread:
      if len(headers) is 0:
        headers = [ x.lower() for x in row ]
      else:
        insertDict(dict(zip(headers, row)), cursor)
  print 'done'

try:
  conn = pg8000.connect(database='csci403', user='dmawhirt', password=getpass.getpass(), host='flowers.mines.edu', port=5432)
  cur = conn.cursor()
  cur.execute('''BEGIN;''')
  loadFile('726160.csv', cur)
  loadFile('726162.csv', cur)
  cur.execute('''COMMIT;''')
  conn.close()
except pg8000.Error as e:
  cur.execute('''ROLLBACK;''')
  print('Database error: ', e.args[2])
  exit()

