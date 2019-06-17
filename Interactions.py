import pyodbc as db


#cursor = DB().CursorConnection()

class intent :
     def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor


     def GetIntent(self , Name):
            # self.conn , cursor = DB().DBconnect()
            command = """
            Select ID From CBT_LKP_Intent Where Name = '{0}'
            """.format(Name)
            try:
                tpl = []
                self.cursor.execute(command)
                for row in self.cursor:
                    tpl.append(row)
            except Exception as e:
                print("Error ", e)
            # DB().DBdisconnect()
            return tpl

     def SaveIntent ( self, name ):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Intent_INS @Name=?
        """
        arg = name
        try:
            self.cursor.execute(command,arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()


     def UpdateIntent(self,id,name):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Intent_UPD @ID=? ,@Name=? 
        """
        arg = (id,name)
        try:
            self.cursor.execute(command,arg)
            print("Updated Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()

     def DeleteIntent(self,id):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Intent_DEL @ID=?
        """
        arg = id
        try:
            self.cursor.execute(command,arg)
            print("Deleted Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()

class slots:
    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor

    def GetIntentSlot(self , IntentName):
        # conn , self.cursor = DB().DBconnect()
        command = """
        Select Slot From CBT_LNK_IntentSlot_VIW Where Intent = '{0}'   
        """.format(IntentName)
        try:
            tpl =[]
            self.cursor.execute(command)
            for row in self.cursor:
                tpl.append(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisconnect()
        return tpl

    def ShowSlots(self):
        # conn , self.cursor = DB().DBconnect()
        command = """
        Select * From CBT_LKP_Slot
        """
        try:
            self.cursor.execute(command)
            for row in self.cursor:
                print(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisconnect()

    def GetSlot(self,name):
        # conn , self.cursor = DB().DBconnect()
        command = """
        Select ID From CBT_LKP_Slot Where Name = '{0}'
        """.format(name)
        try:
            tpl = []
            self.cursor.execute(command)
            for row in self.cursor:
                tpl.append(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisconnect()
        return tpl


    def SaveSlot(self,name):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Slot_INS @Name=? 
        """
        arg =name
        try:
            self.cursor.execute(command,arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()


    def SaveIntentSlot(self,intentID,slotID):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LNK_IntentSlot_INS @IntentID=? , @SlotID=?
        """
        arg =(intentID,slotID)
        try:
            self.cursor.execute(command,arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()


    def UpdateSlot(self,id,name):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Slot_UPD @ID=? ,@Name=? 
        """
        arg = (id,name)
        try:
            self.cursor.execute(command,arg)
            print("Updated Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()



    def UpdateIntentSlot(self,id,intent,slot):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LNK_IntentSlot_UPD @ID=? ,@IntentID=? ,@SlotID=?
        """
        arg = (id,intent,slot)
        try:
            self.cursor.execute(command,arg)
            print("Updated Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisconnect()


    def DeleteSlot(self,id):
        # conn , self.cursor = DB().DBconnect()
        command ="""
        EXEC CBT_LKP_Slot_DEL @ID=?
        """
        arg = id
        try:
            self.cursor.execute(command,arg)
            print("Deleted Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisself.connect()

    def DeleteIntentSlot(self,id):
        # self.conn , self.cursor = DB().DBself.connect()
        command ="""
        EXEC CBT_LNK_IntentSlot_DEL @ID=?
        """
        arg = id
        try:
            self.cursor.execute(command,arg)
            print("Deleted Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ",e)
        # DB().DBdisself.connect()

class logs:
    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor

    def __logs_insert__(self ,Q ):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                  EXEC CBT_Log_INS @Dialoge='{0}'
            """.format(Q)
        # arg = ( Q )
        try:
            self.cursor.execute(command)
            print("Inserted Successfully")
            self.conn.commit()

        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __logs_update__(self, _id ,Q , A ):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          EXEC CBT_Log_UPD @ID=?, @Question=? , @Answer=?
                          """
        arg = (_id , Q , A )
        try:
            self.cursor.execute(command, arg)
            print("Updated Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __logs_delete__(self, _id):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                             EXEC CBT_Log_DEL @ID=?
                             """
        arg = _id
        try:
            self.cursor.execute(command, arg)
            print("Deleted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __logs_selectAll__(self , dialoge):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          select ID from CBT_Log_VIW where Dialoge= '{0}'
                          """.format(dialoge)
        try:
            tpl = []
            self.cursor.execute(command)
            for row in self.cursor:
                print(row[0])
                tpl.append(row)
                print(tpl[0][0])
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()
        return tpl

class feedback:

    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor


    def __feedback_insert__(self , Log_ID, Rate, Message):

        # conn , cursor = DB().DBconnect()
        command = """
               EXEC CBT_Feedback_INS @logID=? , @Rate=? , @Text=?
               """
        arg = (Log_ID, Rate, Message)
        try:
            self.cursor.execute(command, arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisconnect()

    def __feedback_delete__(self, _id):
        # conn , self.cursor = DB().DBconnect()
        command = """
               EXEC CBT_Feedback_DEL @id=?
               """
        arg = _id
        try:
            self.cursor.execute(command, arg)
            print("Deleted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __feedback_update__(self, _id , Log_ID, Rate, Message):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
               EXEC CBT_Feedback_UPD @id=?, @logid=? , @rate=? , @text=?
               """
        arg = (_id, Log_ID, Rate, Message)
        try:
            self.cursor.execute(command, arg)
            print("updated Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

class lowProb:
    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor

    def __lowProb_selectAll__(self):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          select Question , Intent from CBT_LowProb_VIW
                          """
        try:
            self.cursor.execute(command)
            for row in self.cursor:
                print(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __lowProb_selectIntent__(self, ID):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          select * from CBT_LowProb_VIW where IntentID= %d
                          """ % ID

        try:
            self.cursor.execute(command)
            for row in self.cursor:
                print(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __lowProb_insert__(self , Q, IntentID):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                  EXEC CBT_LowProb_INS @Question=?, @IntentID=?
                  """
        arg = (Q, IntentID)
        try:
            self.cursor.execute(command, arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __lowProb_update__(self, _id , Q, IntentID):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          EXEC CBT_LowProb_UPD @ID=?, @Question=?, @IntentID=?
                          """
        arg = (_id, Q, IntentID)
        try:
            self.cursor.execute(command, arg)
            print("Updated Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __lowProb_delete__(self, _id):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                             EXEC CBT_LowProb_DEL @ID=?
                             """
        arg = _id
        try:
            self.cursor.execute(command, arg)
            print("Deleted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

class UnAnswered:
    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor

    def __noIntent_selectAll__(self):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          select Question from CBT_NoIntent_VIW
                          """
        try:
            self.cursor.execute(command)
            for row in self.cursor:
                print(row)
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __noIntent_insert__( self , Q ):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                  EXEC CBT_NoIntent_INS @Question=?
                  """
        arg = Q
        try:
            self.cursor.execute(command, arg)
            print("Inserted Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __noIntent_update__(self, _id , Q):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                          EXEC CBT_NoIntent_UPD @ID=?, @Question=?
                          """
        arg = (_id, Q)
        try:
            self.cursor.execute(command, arg)
            print("Updated Successfully")
            self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()

    def __noIntent_delete__(self, _id):
        # self.conn , self.cursor = DB().DBself.connect()
        command = """
                             EXEC CBT_NoIntent_DEL @ID=?
                             """
        arg = _id
        try:
            self.cursor.execute(command, arg)
            print("Deleted Successfully")
            self.self.conn.commit()
        except Exception as e:
            print("Error ", e)
        # DB().DBdisself.connect()


