from past.builtins import raw_input
import datetime
from User import *
from NLU_Engine import NLU
import pyodbc as db
# from googletrans import Translator
#### Feedback
#### Logs
#### Another Question while asking for entity value
#### Change Yaml entities values to LowerCase
#### Response
# def Translate_Text (question):
#     translator = Translator()
#     translated = translator.translate(question )
#     print("Source Language : " + translated.src)
#     print("Destination Language : " + translated.dest)
#     print("Origin Text : " + translated.origin)
#     print("Translated Text : " + translated.text)
#     return translated.text , translated.src
#     # print("Pronunciation : " + str(translated.pronunciation))

if __name__ == "__main__":
    print("Connecting to Database...")

    #dbconn = db.connect("Driver={SQL SERVER};Server=.;Database=CBT;Trusted_Connection=yes;")
    dbconn = db.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:madyfa.database.windows.net,1433;Database=CBT;Uid=mohamed@madyfa;Pwd={3Oss199755};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cursor = dbconn.cursor()
    flag = 1
    nlu = NLU(dbconn,cursor)
    nlu.EngineMode("Train")
    while (flag):
        question = raw_input("User : ")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        #To End Chat
        if(question == 'q'):
            flag = 0
            break
        # if "feedback" in question or "Feedback" in question or "FeedBack" in question :
        #     print("Chatbot : Please Enter Rank")
        #     rank = int(input("User: "))
        #     print("Chatbot : Please Feel Free to Feedback our Chatbot")
        #     feedback = raw_input("User : ")
        #     print("Chatbot : Thank you for your talk ")
        #     break
        # print(eda(question))

        # nlu.setQuery(Translate_Text(question))
        nlu.setQuery(question)

        nlu.answer()

    print("Disconnecting from Database...")
    cursor.close()
    dbconn.close()




