from Interactions import lowProb , slots , feedback , logs , UnAnswered ,intent

class interaction():

    def __init__(self,conn):
        self.dbconn = conn

    def LogFactory(self):
       return logs(self.dbconn)


    def FeedbackFactory(self):
       return feedback(self.dbconn)

    def LowProbFactory(self):
       return lowProb(self.dbconn)

    def UnAnsweredFactory(self):
        return UnAnswered(self.dbconn)

    def IntentFactory(self):
        return intent(self.dbconn)

    def SlotFactory(self):
        return slots(self.dbconn)

