#!/usr/bin/python

import getpass
import pg8000
import csv

def rm(d, k):
  for x in k:
    if x in d.keys():
      del d[x]
  return d

def insertDicts(table, arr, cursor):
  if len(arr) is 0:
    return
  cols = ','.join(map(lambda x: '"' + x + '"', arr[0].keys()))
  reps = '(' + ','.join([ '(%s)' for x in arr[0].keys() ]) + ')'
  repsarr = []
  valstup = ()
  for d in arr:
    repsarr.append(reps)
    valstup += tuple(d.values())
  stmt = "INSERT INTO %s (%s) VALUES %s;" % (table, cols, ','.join(repsarr))
  cursor.execute(stmt, valstup)

def loadFile(fname, table, cursor, ignore):
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
        rows.append(rm(dict(zip(headers, row)), ignore))
        if len(rows) >= 500:
          insertDicts(table, rows, cursor)
          rows = []
    insertDicts(table, rows, cursor)
  print 'done'

try:
  conn = pg8000.connect(database='csci403', user='dmawhirt', password=getpass.getpass(), host='flowers.mines.edu', port=5432)
  cur = conn.cursor()
  cur.execute('''BEGIN;''')
  cur.execute('''DROP TABLE IF EXISTS weather;''')
  cur.execute('''CREATE TABLE weather ( station text, station_name text, elevation real, latitude numeric, longitude numeric, date date, mdpr numeric, mdsf numeric, dapr numeric, prcp numeric, snwd numeric, snow numeric, tmax numeric, tmin numeric, tobs numeric, awnd numeric);''')
  cur.execute('''DROP TABLE IF EXISTS dond;''')
  cur.execute('''CREATE TABLE dond ( id text, broadcast_date date, name text, education char, gender char, age int, stop_round int, amount_won int, round int, deal_or_no_deal text, "bank-offer" int, "0.01" boolean, "1" boolean, "5" boolean, "10" boolean, "25" boolean, "50" boolean, "75" boolean, "100" boolean, "200" boolean, "300" boolean, "400" boolean, "500" boolean, "750" boolean, "1,000" boolean, "5,000" boolean, "10,000" boolean, "25,000" boolean, "50,000" boolean, "75,000" boolean, "100,000" boolean, "200,000" boolean, "300,000" boolean, "400,000" boolean, "500,000" boolean, "750,000" boolean, "1,000,000" boolean, "1,500,000" boolean );''')
  loadFile('DOND1.csv', 'dond', cur, [])
  loadFile('DOND2.csv', 'dond', cur, [])
  loadFile('726160.csv', 'weather', cur, ['dasf'])
  loadFile('726162.csv', 'weather', cur, ['dasf'])
  cur.execute('''COMMIT;''')
  conn.close()
except pg8000.Error as e:
  cur.execute('''ROLLBACK;''')
  print('Database error: ', e.args[2])
  exit()

