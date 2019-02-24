from User import User
from NLU_Engine import NLU

nlu = NLU()

nlu.setQuaery('give me my gpa')

print(nlu.checkSlot())



