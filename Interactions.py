from DBConnection import Database as DB


cursor = DB().CursorConnection()

class intent :
     def __init__(self , conn):
            self.DBconn = conn
            print("Intent")

     def GetIntent(self , Name):

            command = """
            Select ID From CBT_LKP_Intent Where Name = '{0}'
            """.format(Name)
            try:
                tpl = []
                cursor.execute(command)
                for row in cursor:
                    tpl.append(row)
            except Exception as e:
                print("Error ", e)
            return tpl

     def SaveIntent ( self, name ):
        command ="""
        EXEC CBT_LKP_Intent_INS @Name=?
        """
        arg = name
        try:
            cursor.execute(command,arg)
            print("Inserted Successfully")
            self. DBconn.commit()
        except Exception as e:
            print("Error ",e)


     def UpdateIntent(self,id,name):
        command ="""
        EXEC CBT_LKP_Intent_UPD @ID=? ,@Name=? 
        """
        arg = (id,name)
        try:
            cursor.execute(command,arg)
            print("Updated Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)

     def DeleteIntent(self,id):
        command ="""
        EXEC CBT_LKP_Intent_DEL @ID=?
        """
        arg = id
        try:
            cursor.execute(command,arg)
            print("Deleted Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)

class slots():


    def __init__(self,conn):
        self.DBconn = conn
        print("Slot")

    def GetIntentSlot(self , IntentName):
        command = """
        Select Slot From CBT_LNK_IntentSlot_VIW Where Intent = '{0}'   
        """.format(IntentName)
        try:
            tpl =[]
            cursor.execute(command)
            for row in cursor:
                tpl.append(row)
        except Exception as e:
            print("Error ", e)
        return tpl

    def ShowSlots(self):
        command = """
        Select * From CBT_LKP_Slot
        """
        try:
            cursor.execute(command)
            for row in cursor:
                print(row)
        except Exception as e:
            print("Error ", e)

    def GetSlot(self,name):
        command = """
        Select ID From CBT_LKP_Slot Where Name = '{0}'
        """.format(name)
        try:
            tpl = []
            cursor.execute(command)
            for row in cursor:
                tpl.append(row)
        except Exception as e:
            print("Error ", e)
        return tpl


    def SaveSlot(self,name):
        command ="""
        EXEC CBT_LKP_Slot_INS @Name=? 
        """
        arg =name
        try:
            cursor.execute(command,arg)
            print("Inserted Successfully")
            self.DBconn.commit()
        except Exception as e:
            print("Error ",e)


    def SaveIntentSlot(self,intentID,slotID):

        command ="""
        EXEC CBT_LNK_IntentSlot_INS @IntentID=? , @SlotID=?
        """
        arg =(intentID,slotID)
        try:
            cursor.execute(command,arg)
            print("Inserted Successfully")
            self.DBconn.commit()
        except Exception as e:
            print("Error ",e)


    def UpdateSlot(self,id,name):

        command ="""
        EXEC CBT_LKP_Slot_UPD @ID=? ,@Name=? 
        """
        arg = (id,name)
        try:
            cursor.execute(command,arg)
            print("Updated Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)




    def UpdateIntentSlot(self,id,intent,slot):

        command ="""
        EXEC CBT_LNK_IntentSlot_UPD @ID=? ,@IntentID=? ,@SlotID=?
        """
        arg = (id,intent,slot)
        try:
            cursor.execute(command,arg)
            print("Updated Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)


    def DeleteSlot(self,id):
        command ="""
        EXEC CBT_LKP_Slot_DEL @ID=?
        """
        arg = id
        try:
            cursor.execute(command,arg)
            print("Deleted Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)


    def DeleteIntentSlot(self,id):
        command ="""
        EXEC CBT_LNK_IntentSlot_DEL @ID=?
        """
        arg = id
        try:
            cursor.execute(command,arg)
            print("Deleted Successfully")
            self.DBconn.commit()

        except Exception as e:
            print("Error ",e)

class logs:

    def __init__(self,conn):
        self.connection = conn
        print("Logs")

    def __logs_insert__(self ,Q , A ):
        command = """
                  EXEC CBT_Log_INS @Question=? , @Answer=?
                  """
        arg = ( Q , A )
        try:
            cursor.execute(command, arg)
            print("Inserted Successfully")
            self.connection.commit()

        except Exception as e:
            print("Error ", e)

    def __logs_update__(self, _id ,Q , A ):
        command = """
                          EXEC CBT_Log_UPD @ID=?, @Question=? , @Answer=?
                          """
        arg = (_id , Q , A )
        try:
            cursor.execute(command, arg)
            print("Updated Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __logs_delete__(self, _id):
        command = """
                             EXEC CBT_Log_DEL @ID=?
                             """
        arg = _id
        try:
            cursor.execute(command, arg)
            print("Deleted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

class feedback:

    def __init__(self,conn):
        self.connection = conn
        print("FeedBack")

    def __feedback_insert__(self , Log_ID, Rate, Message):
        command = """
               EXEC CBT_Feedback_INS @logid=? , @rate=? , @text=?
               """
        arg = (Log_ID, Rate, Message)
        try:
            cursor.execute(command, arg)
            print("Inserted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __feedback_delete__(self, _id):
        command = """
               EXEC CBT_Feedback_DEL @id=?
               """
        arg = _id
        try:
            cursor.execute(command, arg)
            print("Deleted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __feedback_update__(self, _id , Log_ID, Rate, Message):
        command = """
               EXEC CBT_Feedback_UPD @id=?, @logid=? , @rate=? , @text=?
               """
        arg = (_id, Log_ID, Rate, Message)
        try:
            cursor.execute(command, arg)
            print("updated Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

class lowProb:
    def __init__(self,conn):
        self.connection = conn
        print("Low Probability")

    def __lowProb_selectAll__(self):
        command = """
                          select Question , Intent from CBT_LowProb_VIW
                          """
        try:
            cursor.execute(command)
            for row in cursor:
                print(row)
        except Exception as e:
            print("Error ", e)

    def __lowProb_selectIntent__(self, ID):
        command = """
                          select * from CBT_LowProb_VIW where IntentID= %d
                          """ % ID

        try:
            cursor.execute(command)
            for row in cursor:
                print(row)
        except Exception as e:
            print("Error ", e)

    def __lowProb_insert__(self , Q, IntentID):
        command = """
                  EXEC CBT_LowProb_INS @Question=?, @IntentID=?
                  """
        arg = (Q, IntentID)
        try:
            cursor.execute(command, arg)
            print("Inserted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __lowProb_update__(self, _id , Q, IntentID):
        command = """
                          EXEC CBT_LowProb_UPD @ID=?, @Question=?, @IntentID=?
                          """
        arg = (_id, Q, IntentID)
        try:
            cursor.execute(command, arg)
            print("Updated Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __lowProb_delete__(self, _id):
        command = """
                             EXEC CBT_LowProb_DEL @ID=?
                             """
        arg = _id
        try:
            cursor.execute(command, arg)
            print("Deleted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

class UnAnswered:

    def __init__(self,conn):
        self.connection = conn
        print("No Intent")

    def __noIntent_selectAll__(self):
        command = """
                          select Question from CBT_NoIntent_VIW
                          """
        try:
            cursor.execute(command)
            for row in cursor:
                print(row)
        except Exception as e:
            print("Error ", e)

    def __noIntent_insert__( self , Q ):
        command = """
                  EXEC CBT_NoIntent_INS @Question=?
                  """
        arg = Q
        try:
            cursor.execute(command, arg)
            print("Inserted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __noIntent_update__(self, _id , Q):
        command = """
                          EXEC CBT_NoIntent_UPD @ID=?, @Question=?
                          """
        arg = (_id, Q)
        try:
            cursor.execute(command, arg)
            print("Updated Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)

    def __noIntent_delete__(self, _id):
        command = """
                             EXEC CBT_NoIntent_DEL @ID=?
                             """
        arg = _id
        try:
            cursor.execute(command, arg)
            print("Deleted Successfully")
            self.connection.commit()
        except Exception as e:
            print("Error ", e)


