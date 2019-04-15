from past.builtins import raw_input

from User import User
from NLU_Engine import NLU

#### Feedback
#### Logs
#### Another Question while asking for entity value
#### Change Yaml entities values to LowerCase
#### Response


if __name__ == "__main__":

    flag = 1
    nlu = NLU()
    nlu.EngineMode("Train")
    while (flag):
        question = raw_input("User : ")

        #To End Chat
        if(question == 'q'):
            flag = 0
            break

        nlu.setQuery(question)

        nlu.answer()




