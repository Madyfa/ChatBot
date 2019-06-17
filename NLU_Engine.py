import io
import json
import random
import re
# import pandas as pd
# import snips_nlu_en
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
# from googletrans import Translator
import datetime
from DBConnection import Database
from DB_Interaction import interaction

class NLU:

    # def __Translate_Text (question,x='en'):
    #     translator = Translator()
    #     translated = translator.        translate(question , dest=x)
    #     print("Source Language : " + translated.src)
    #     print("Destination Language : " + translated.dest)
    #     print("Origin Text : " + translated.origin)
    #     print("Translated Text : " + translated.text)
    #     return translated.text

    def __init__(self , dbconn ,cursor):
        self._query = ''
        self.__result = ''
        self._intent = ''
        self._probability = 0
        self._slots = {}
        self.__interaction = interaction(dbconn ,cursor)
        self.__engine=''
        self.__dataset=''
        self.__nluSlots=''
        self.language=''
        self.logs = ''

    with io.open("Responses.json") as f:
               response = json.load(f)

    def EngineMode(self, mode):
        """
        Saving the engine to use the model for every question (Training Part)
        or Use the model if it already exists (Testing Part)

        :param mode: Test or Train string
        :return:  Fitted Engine
        """


        if mode =="Train":
            load_resources('snips_nlu_en')

            self.__engine = SnipsNLUEngine(config=CONFIG_EN)
            with io.open("dataset.json") as f:
               self.__dataset = json.load(f)

            self.__engine.fit(self.__dataset)

            #UnComment to save the model
            #self.__engine.persist("Z:\FCIS-ASU\Semester 8\ChatbotModel")

        elif mode =="Test":
            with io.open("dataset.json") as f:
               self.__dataset = json.load(f)
            self.__engine = SnipsNLUEngine.from_path("Z:\FCIS-ASU\Semester 8\ChatbotModel")



    def setQuery(self, query):
        # self._query , self.language = query
        self._query = query.strip()
        self.__excute()



    def __excute(self):
        parsing = self.__engine.parse(self._query)
        self.__result = json.loads(json.dumps(parsing,indent=2))
        if self._query.__contains__("'"):
            self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : "+self._query.replace("'","/") +"\n")
        print( self.__result )

    def _getIntent(self):
        try:
            self._intent = self.__result['intent']['intentName']
            return self._intent
        except Exception as e:
            return 'None'


    def _getProbability(self):
        self._probability = self.__result['intent']['probability']
        return self._probability

    #need Handling Exception
    def _getSlots(self):
        dic = {}
        if len(self.__result['slots']) != 0:
            if self.CheckValinIntent():
                for x in range(len(self.__result['slots'])):
                    if not re.search("Val",self.__result['slots'][x]['entity']):
                        if str(self.__result['slots'][x]['entity']).__contains__("snips"):
                            dic[self.__result['slots'][x]['slotName']] = self.__result['slots'][x]['value']['value']
                        else:
                            dic[self.__result['slots'][x]['entity']] = self.__result['slots'][x]['value']['value']
            else:
                return "No Slots"
        else:
            return "No Slots"

        self._slots = dic
        return self._slots


    def checkIntent(self):
        if self._getIntent() == 'None':
            try:
                self.__interaction.UnAnsweredFactory().__noIntent_insert__(self._query)
            except Exception as e:
                print("Error ", e)
            return False
        else:
            return True


    def answer(self):
        """
             Check if the question has intent or None

        :return: Answer
        """
        

        if self.checkIntent():
            if str(self.CheckJsonEntities()).__contains__("Has No Entities"):
                print("Chatbot : ",random.choice(self.response['intents'][self._getIntent()]))
                print("Chatbot : Get Answer From Json Answers")
            elif str(self.CheckJsonEntities()).__contains__("Has No Intent"):
                 self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" ChatBot : Not Available due to SmallTalk intent" +"\n")
                 print('ChatBot : not available due to SmallTalk intent')
            else:
                self.return_original()
        else:
            self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" ChatBot : Not Available due to intent" +"\n")
            print('ChatBot : not available due to intent')

    def checkSlots(self):
        self.__nluSlots = self._getSlots()
        if str(self.__nluSlots).__contains__("No Slots") :
            return "No"
        datasetSlots = []
        for i in range(len(self.__dataset['intents'][self._getIntent()]['utterances'])):
            for j in range(len(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'])):
                check = json.dumps(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'][j])
                if 'entity' in check:
                    if str(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'][j]['entity']).__contains__("snips"):
                        datasetSlots.append(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'][j]['slot_name'])
                    else:
                        datasetSlots.append(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'][j]['entity'])
                    datasetSlots = list(dict.fromkeys(datasetSlots))
        for x in datasetSlots:
            if 'Val' in x:
                datasetSlots.remove(x)
        ret = []
        for i in range(len(datasetSlots)):
            found = False
            for j in self.__nluSlots.keys():
                if datasetSlots[i] == j:
                    found = True
                    break
            if not found:
                ret.append(datasetSlots[i])
        # print("Slots Not Available in Question : ", ret)  # el mafroud btalla3 el slots ely mesh mwgooda
        return ret


    def askForunenteredEntities(self):
        slots_needed = self._getSlots()
        # print(slots_needed)
        slots_missing = self.checkSlots()
        if str(slots_missing).__contains__("No"):
            return
        loopflagi = True
        # print(temp3[1]);
        for i in range(len(slots_missing)):
            loopflagi = False
            while not loopflagi:
                chatbotques = random.choice(self.response['entities'][str(slots_missing[i])])
                # chatbotques = "Please Enter "+slots_missing[i]
                # chatbotques = self.response['entities'][str(slots_missing[i])]
                # g = Translator().translate(chatbotques , dest = self.language).text
                # print("Chatbot: ",g)
                self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" ChatBot : "+ chatbotques +"\n")
                print ("Chatbot : ",chatbotques)

                values=[]
                # print("Chatbot: Possible Values for", slots_missing[i], "are:")
                for k in range(len(self.__dataset['entities'][slots_missing[i]]['data'])):
                            values.append(self.__dataset['entities'][slots_missing[i]]['data'][k]['value'])
                print(values)
                reply = input("User: ")
                if reply.strip() == 'q':
                    self.__nluSlots = "return"
                    break

                if reply.__contains__("'"):
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : "+reply.replace("'","/") +"\n")
                else:
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : "+reply +"\n")


                for j in range(len(self.__dataset['entities'][slots_missing[i]]['data'])):
                    try:
                        check = json.dumps(self.__dataset['entities'][slots_missing[i]]['data'][j])
                        print(check)
                    except:
                        continue
                    if self.match(reply.strip(),check):
                        # e3ml 7aga
                        self.__nluSlots[slots_missing[i]] = reply.strip()

                        loopflagi = True
                        break
                # if not loopflagi:
                #     x = slots_missing
                #     self.setQuery(reply)
                #     if self.checkIntent():
                #         self.answer()
                #         return "Second Try"
                #     else:
                #         slots_missing = x
                #         print("Chatbot : I can't understand you")
                #
            if self.__nluSlots ==  "return":
                break
        return self.__nluSlots

    def match(self, reply, check):
        i = 0
        while i < len(check):
            if check[i] == '"':
                curr = ""
                j = i + 1
                while j < len(check) and check[j] != '"':
                    curr = curr + check[j]
                    j = j+1
                if curr == reply and reply != "synonyms" and reply != "value":
                    return True
            i = i+1
        return False

    def return_original(self):
        slots_needed = self.askForunenteredEntities()
        if slots_needed == "return":
            return
        if slots_needed is None:
            try:
                self.__interaction.UnAnsweredFactory().__noIntent_insert__(self._query)
            except Exception as e:
                print("Error ", e)
            self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : I dont have answer for this"+"\n")
            print("ChatBot : I don't have answer for this")
            return
        if self._getIntent() == "Feedback":
            self.feedback_msg()
            return
        key_list = list(slots_needed.keys())

        # print(key_list)
        finaldic = dict()
        for key in range(len(key_list)):
            # print(key_list[key] + "here")
            # print(slots_needed[key_list[key]])
            # do something
            if key_list[key] == "ID":
                continue
            # print("Key :",key_list[key])

            try:
                for i in range(len(self.__dataset['entities'][key_list[key]]["data"])):
                    check = json.dumps(self.__dataset['entities'][key_list[key]]["data"][i])
                    if slots_needed[key_list[key]] in check:
                        self.__nluSlots[key_list[key]] = self.__dataset['entities'][key_list[key]]["data"][i]["value"]
                        # print(self.__dataset['entities'][key_list[key]]["data"][i]["value"])
            except:
                print("Error")

        self.GetAnswerFromDB(self.__nluSlots)
        # print("Values to get from Database" , self.__nluSlots)  # original values of entities used in question
        # return List or dictionary??

    def GetAnswerFromDB(self,slots):
        command = "Select Answer From CBT_"+self._getIntent()+" where "
        flag = True
        for key, value in slots.items():
            if flag:
                 command +=key+" = '"+value.lower()+"'"
                 flag=False
            else:
                 command +=" and "+key + " = '"+value.lower()+"'"
        # print(random.choice(self.response['intents'][str(self._getIntent())]) +command)
        try:
            answe = self.__interaction.DatabaseFactory("answer").GetAnswer(command)
            if answe == '':
                 self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Sorry I don't have this answer " + "\n")
                 print("Sorry I don't have this answer ")
            else:
                self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : "+ random.choice(self.response['intents'][str(self._getIntent())]) + answe[0][0] + "\n")
                print("Chatbot : ",random.choice(self.response['intents'][str(self._getIntent())]) + answe[0][0])
        except :
            self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Sorry I dont have this answer")
            print("Sorry I don't have this answer ")

    def CheckJsonEntities(self):
         for i in range(len(self.__dataset['intents'][self._getIntent()]['utterances'])):
                for j in range(len(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'])):
                    check = json.dumps(self.__dataset['intents'][self._getIntent()]['utterances'][i]['data'][j])
                    # print(check)
                    if 'entity' in check:
                        # print("Entities")
                        return "Has Entities"

                # print("-----------")
         # print("Exit with No Entities")
         if self._getProbability() >= 0.4:
             return "Has No Entities"
         else:
             return "Has No Intent"

    def CheckValinIntent(self):
        for x in range(len(self.__result['slots'])):
                if re.search("Val",self.__result['slots'][x]['entity']):
                    return True
        return False

    def feedback_msg(self):
        feedback_Msg = ''
        rank = ''
        rankvalues=[1,2,3,4,5]
        self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Enter The Rank "+"\n")
        print("Chatbot : Please Enter The Rank ")
        while True :
            try:
                print(rankvalues)
                rank = int(input("User: "))
                if  0 < rank < 6 :
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Enter a Number From 1 to 5 "+"\n")
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : "+str(rank)+"\n")
                    break
                else:
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Enter a Number From 1 to 5 "+"\n")
                    print("Chatbot: Please Enter a Number From 1 to 5 ")
                    continue
            except:
                self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Enter a Number "+"\n")
                print("Chatbot: Please Enter a Number")
                continue
        self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Feel Free to Feedback our Chatbot "+"\n")
        print("Chatbot : Please Feel Free to Feedback our Chatbot")
        while feedback_Msg == '':
                feedback_Msg = input("User : ")
                if feedback_Msg == '':
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : NULL"+"\n")
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Please Enter a Message "+"\n")
                    print("Chatbot: Please Enter a Message")
                    continue
                else:
                    self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" User : "+feedback_Msg+"\n")
                    break
        self.logs += ("[ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ] "+" Chatbot : Thanks for your Feedback "+"\n")
        print("Chatbot : Thanks for your Feedback")
        try:
            self.__interaction.LogFactory().__logs_insert__(str(self.logs))
            print(self.logs)
            log_id = self.__interaction.LogFactory().__logs_selectAll__(str(self.logs))
            print(int(log_id[0][0]))
            print(int(rank))
            self.__interaction.FeedbackFactory().__feedback_insert__(int(log_id[0][0]) , int(rank) , feedback_Msg)

        except Exception as e:
            print("Error ", e)
