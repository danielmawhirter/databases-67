#!/usr/bin/python

import getpass
import pg8000
import csv

def insertDicts(arr, cursor):
  if len(arr) is 0:
    return
  if 'dasf' in arr[0]:
    del arr[0]['dasf']
  cols = ','.join(arr[0].keys())
  reps = '(' + ','.join([ '(%s)' for x in arr[0].keys() ]) + ')'
  repsarr = []
  valstup = ()
  for d in arr:
    if 'dasf' in d:
      del d['dasf']
    repsarr.append(reps)
    valstup += tuple(d.values())
  stmt = "INSERT INTO weather (%s) VALUES %s;" % (cols, ','.join(repsarr))
  cursor.execute(stmt, valstup)

def loadFile(fname, cursor):
  print 'loading: ' + fname
  with open(fname) as f:
    csvread = csv.reader(f)
    headers = []
    rows = []
    for row in csvread:
      if len(headers) is 0:
        headers = [ x.lower() for x in row ]
      else:
        if 'unknown' in row:
          continue
        rows.append(dict(zip(headers, row)))
        if len(rows) >= 500:
          insertDicts(rows, cursor)
          rows = []
    insertDicts(rows, cursor)
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

