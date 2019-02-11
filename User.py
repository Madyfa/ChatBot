class User:
    def __int__(self):
        self.__query = ''
        self.__feedback = ''
        self.__rate = 0

    def setQuery(self):
        self.__query = input('You: ')
        return self.__query


    def setFeedback(self, feedback):
        self.feedback = feedback

    def setRate(self, rate):
        self.rate = rate



