import pyodbc as db

dbconn = db.connect("Driver={SQL SERVER};Server=.;Database=CBT;Trusted_Connection=yes;")
cursor = dbconn.cursor()

class Database:

    def DBconnect(self):
        print("Connecting to Database...")
        return dbconn

    def CursorConnection(self):
        return cursor

    def DBdisconnect(self):
        print("Disconnecting from Database...")
        cursor.close()
        dbconn.close()
