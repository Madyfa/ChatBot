import io
import json
import snips_nlu_en
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN

load_resources('snips_nlu_en')

engine = SnipsNLUEngine(config=CONFIG_EN)

with io.open("dataset.json") as f:
    dataset = json.load(f)

engine.fit(dataset)


class NLU:
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
        self._intent = self.__result['intent']['intentName']
        return self._intent

    def _getProbability(self):
        self._probability = self.__result['intent']['probability']
        return self._probability

    def _getSlots(self):
        dic = {}
        if len(self.__result['slots']) != 0:
            for x in range(len(self.__result['slots'])):
                dic[self.__result['slots'][x]['entity']] = self.__result['slots'][x]['rawValue']

        self._slots = dic
        return self._slots

