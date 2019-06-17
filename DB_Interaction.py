from Interactions import lowProb , slots , feedback , logs , UnAnswered ,intent ,Answer

class interaction():

    def __init__(self, dbconn,cursor):
        self.conn = dbconn
        self.cursor = cursor

    def DatabaseFactory(self,tablename):
        if tablename =="feedback":
            return feedback(self.conn,self.cursor)
        elif tablename =="logs":
            return logs(self.conn,self.cursor)
        elif tablename =="unanswered":
            return UnAnswered(self.conn,self.cursor)
        elif tablename =="answer":
            return Answer(self.conn,self.cursor)

    def LogFactory(self):

       return logs(self.conn,self.cursor)


    def FeedbackFactory(self):
       return feedback(self.conn,self.cursor)

    def LowProbFactory(self):
       return lowProb(self.conn,self.cursor)

    def UnAnsweredFactory(self):
        return UnAnswered(self.conn,self.cursor)

    def IntentFactory(self):
        return intent(self.conn,self.cursor)

    def SlotFactory(self):
        return slots(self.conn,self.cursor)


#interaction().SlotFactory().SaveSlot('CourseName')
#interaction().IntentFactory().SaveIntent('ReqCourseDescription')
#intent = interaction().IntentFactory().GetIntent('ReqCourseDescription')
#slot = interaction().SlotFactory().GetSlot('CourseName')
#interaction().SlotFactory().SaveIntentSlot(intent[0][0],slot[0][0])

#x = (interaction().SlotFactory().GetIntentSlot('ReqSchedule'))
#interaction().SlotFactory().DeleteIntentSlot(1005)
#print(x[0][0])
