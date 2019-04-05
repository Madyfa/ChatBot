import io
import json
import snips_nlu_en
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN

from DBConnection import Database
from DB_Interaction import interaction

load_resources('snips_nlu_en')

engine = SnipsNLUEngine(config=CONFIG_EN)

with io.open("dataset.json") as f:
    dataset = json.load(f)

engine.fit(dataset)


class NLU:
    __connection = Database()
    __interaction = interaction(__connection.DBconnect())

    def __int__(self):
        self._query = ''
        self.__result = ''
        self._intent = ''
        self._probability = 0
        self._slots = {}


    def setQuaery(self, query):
        self._query = query
        self.__excute()

    def __excute(self):
        parsing = engine.parse(self._query)
        self.__result = json.loads(json.dumps(parsing))

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
            for x in range(len(self.__result['slots'])):
                dic[self.__result['slots'][x]['entity']] = self.__result['slots'][x]['rawValue']

        self._slots = dic
        return self._slots


    def checkIntent(self):
        if self._getIntent() == 'None':
            self.__interaction.UnAnsweredFactory().__noIntent_insert__(self._query)
            return False
        elif self._getProbability() < 0.7:
            intentID = self.__interaction.IntentFactory().GetIntent(self._getIntent())
            self.__interaction.LowProbFactory().__lowProb_insert__(self._query, intentID)
            return False
        else:
            return True

    # def checkSlot(self):
    #     dbSlots = self.__interaction.SlotFactory().GetIntentSlot(self._getIntent())
    #     nluSlots = self._getSlots()
    #     #dbSlots = ['gpa', 'ID', 'Department']
    #     ret = []
    #
    #     for i in range(len(dbSlots)):
    #         for j in nluSlots:
    #             if dbSlots[i] == j:
    #                 break
    #             else:
    #                 ret.append(dbSlots[i])
    #
    #     return ret

    def answer(self):
        slots = self.checkSlot()
        if self.checkIntent():
            if slots is not None:
                s = 'Enter '
                for i in slots:
                    s += str(i) + ', '
                print(s)
            else:

                print('get the answers from database')
        else:
            print('not available due to intent')

    def checkSlots(self):
        datasetSlots = []
        print(self._getIntent())
        for i in range(len(dataset['intents'][self._getIntent()]['utterances'])):
            for j in range(len(dataset['intents'][self._getIntent()]['utterances'][i]['data'])):
                check = json.dumps(dataset['intents'][self._getIntent()]['utterances'][i]['data'][j])
                if 'entity' in check:
                    datasetSlots.append(dataset['intents'][self._getIntent()]['utterances'][i]['data'][j]['entity'])
                    datasetSlots = list(dict.fromkeys(datasetSlots))
        for x in datasetSlots:
            if 'Val' in x:
                datasetSlots.remove(x)
        nluSlots = self._getSlots()
        ret = []
        for i in range(len(datasetSlots)):
            found = False
            for j in nluSlots.keys():
                if datasetSlots[i] == j:
                    found = True
                    break
            if not found:
                ret.append(datasetSlots[i])
        print("Slots Not Available in Question : ", ret)  # el mafroud btalla3 el slots ely el mafroud tb2a mwgooda
        return ret

    def askForunenteredEntities(self):
        slots_needed = self._getSlots()
        print(slots_needed)
        slots_missing = self.checkSlots()
        loopflagi = True
        # print(temp3[1]);
        for i in range(len(slots_missing)):
            loopflagi = False
            while not loopflagi:
                print("Chatbot: Please Enter", slots_missing[i])
                reply = raw_input("User: ")
                if reply == 'q':
                    break
                for j in range(len(dataset['entities'][slots_missing[i]])):
                    try:
                        check = json.dumps(dataset['entities'][slots_missing[i]]['data'][j])
                    except:
                        continue
                    if reply in check:
                        # e3ml 7aga
                        slots_needed[slots_missing[i]] = reply
                        loopflagi = True
                        break
        return slots_needed

    def return_original(self):
        slots_needed = self.askForunenteredEntities()
        key_list = list(slots_needed.keys())
        finaldic = dict()
        for key in range(len(key_list)):
            # print(key_list[key] + "here")
            # print(slots_needed[key_list[key]])
            # do something
            for i in range(len(dataset['entities'][key_list[key]]["data"])):
                check = json.dumps(dataset['entities'][key_list[key]]["data"][i])
                if slots_needed[key_list[key]] in check:
                    finaldic[key_list[key]] = dataset['entities'][key_list[key]]["data"][i]["value"]
                    # print(dataset['entities'][key_list[key]]["data"][i]["value"])
        print(finaldic)  # original values of entities used in question
        # return List or dictionary??
