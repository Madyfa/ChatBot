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

    def checkSlot(self):
        dbSlots = self.__interaction.SlotFactory().GetIntentSlot(self._getIntent())
        nluSlots = self._getSlots()
        #dbSlots = ['gpa', 'ID', 'Department']
        ret = []

        for i in range(len(dbSlots)):
            for j in nluSlots:
                if dbSlots[i] == j:
                    break
                else:
                    ret.append(dbSlots[i])

        return ret

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

