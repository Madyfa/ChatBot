# from User import User
# from NLU_Engine import NLU
#
# nlu = NLU()
#
# nlu.setQuaery('give me my gpa')
#
# # print(nlu.checkSlot())
#
#
#

from past.builtins import raw_input

from User import User
from NLU_Engine import NLU




if __name__ == "__main__":

    flag = 1
    nlu = NLU()
    while (flag):
        question = raw_input("User : ")

        #To End Chat
        if(question == 'q'):
            flag = 0
            break

        nlu.setQuery(question)


