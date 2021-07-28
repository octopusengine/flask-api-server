import sys, traceback, datetime, sqlite3

DB3 = "agama3.db"
FLOG = "log.txt"
FMSG = "msg01.txt"

def db_init():
  try:
    sqliteConnection = sqlite3.connect(DB3)
    sqlite_create_table_query = '''CREATE TABLE log (id INTEGER PRIMARY KEY,
                                logdatetime timestamp, place TEXT NOT NULL,
                                note TEXT, key TEXT);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

  except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
  finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")


def db_log_add(place="?"):
  try:
    sqliteConnection = sqlite3.connect(DB3)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    dtn = datetime.datetime.now()
    sqlite_insert_query = "INSERT INTO log (id, logdatetime, place) VALUES (null, ?, ?)"

    count = cursor.execute(sqlite_insert_query, (dtn,place))
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

  except sqlite3.Error as error:
    print("Failed to insert data into sqlite table")
    print("Exception class is: ", error.__class__)
    print("Exception is", error.args)
    print('Printing detailed SQLite exception traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
  finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("The SQLite connection is closed")


def db_read():
    try:
        sqliteConnection = sqlite3.connect(DB3, timeout=20)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT count(*) from log"""
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchone()
        print("Total rows are:  ", totalRows)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The Sqlite connection is closed")

def db_log_print():
  conn = sqlite3.connect(DB3)
  print("Opened database successfully")

  cursor = conn.execute("SELECT id, logdatetime, place from log")
  for row in cursor:
     print("ID: ", row[0], "DAT_TIME: ", row[1], "PLACE: ", row[2])

  print("Operation done successfully")
  conn.close()


def db_log_list():
  conn = sqlite3.connect(DB3)
  print("Opened database successfully")

  log_list = []
  cursor = conn.execute("SELECT id, logdatetime, place from log ORDER BY logdatetime DESC LIMIT 50")
  for row in cursor:
     #print("ID: ", row[0], "DAT_TIME: ", row[1], "PLACE: ", row[2])
     log_list.append(str(row[1])[:19] + " | " +row[2])
  print("Operation done successfully")
  conn.close()
  return log_list


def add_log_txt(log="-"):
   f = open(FLOG, "a")
   ra = remote_addr()
   dt = str(datetime.datetime.now())
   f.write(dt + "; "+ log + " | "+ ra +"\n")
   f.close()


def add_msg_txt(nick="?",msg="-"):
   f = open(FMSG, "a")
   dt = str(datetime.datetime.now())[:19]
   f.write(dt + " | "+ nick[:32] + " | "+ msg[:80] +"\n")
   f.close()


def tail_msg_txt(num=12):
   f = open(FMSG,"r")
   lines = f.readlines()
   cnt = len(lines)
   if num>cnt: num=cnt-1
   rs = "\n"
   for i in range(num):
      rs += lines[cnt-i-1]
   rs += "..."
   return rs


def tail_log_txt(num=20):
   f = open(FLOG,"r")
   lines = f.readlines()
   cnt = len(lines)
   if num>cnt: num=cnt-1
   rs = "\n .:. log.cnt: " + str(num) + "/" + str(cnt) + "\n"
   for i in range(num):
      rs += lines[cnt-i-1]
   rs += "..."
   return rs
