import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

def switch(mood):
    switcher = {
        "happy": "sad",
        "sad": "happy",
        "anger": "noemo",
        "surprise": "noemo",
        "disgust": "noemo",
        "fear": "noemo"
    }

    return switcher.get(mood, "noemo")

def syn_check(word):
    happy = ["happy", "content", "cheery", "merry", "joyful", "jovial", "jolly", "joke", "glee", "carefree", "untroubled", "delighted","smiled", "stoke", "perfect", "great", "amaz", "wonderful"]
    sad = ["sad", "unhappy", "horrible", "disappoint", "sorrow", "deject", "regret", "depress", "downcast", "miserable", "downhearted", "despondent", "despair", "disconsolate", "out of sorts", "desolate", "gloomy", "dismal", "heartbroken", "crying"]
    fear = ["scar", "terror", "fright" "panic", "agitate", "dread", "anxiety", "worry", "unease", "alarm"]
    anger = ["angry", "annoy", "irritate", "exasperate", "fury", "vex", "provoke"]
    disgust = ["disgust", "repulse", "sicken", "nauseate"]
    surprise = ["wow", "shock", "surprise", "astonish", "amaze", "startle"]
    no = ["not", "neither"]

    mood = "none"

    if any(x in word for x in happy):
        mood = "happy"

    elif any(x in word for x in sad):
        mood = "sad"

    elif any(x in word for x in anger):
        mood = "anger"

    elif any(x in word for x in surprise):
        mood = "surprise"

    elif any(x in word for x in disgust):
        mood = "disgust"

    elif any(x in word for x in fear):
        mood = "fear"

    elif any(x in word for x in no):
        mood = "not"

    else:
        mood = "none"

    return mood

def syn_final(l):
    cnot = 0
    for i in l:
        if (i == "none"):
            l.remove(i)
        elif (i == "not"):
            cnot = cnot+1
            l.remove(i)
        else:
            pass
    if (len(l) == 0):
        res = "none"
    else:
        f = max(set(l), key=l.count)
        if(cnot == 0):
            res = f
        else:
            res = switch(f)

    return res
    


class SynonymChecker(Component):

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""

        return []

    defaults = {}
    supported_language_list = None
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(SynonymChecker, self).__init__(component_config)
    
    def convert_to_rasa(self, value, confidence):
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "synonym",
                  "extractor": "synonym_checker"}

        return entity

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        l = []
        try:
            w = message.data['text'].split(" ")
            for word in w:
                l.append(syn_check(word))
            res = syn_final(l)
            entity = self.convert_to_rasa(res, 1)
            message.set("synonym", [entity], add_to_output=True)
        except KeyError:
            pass
        pass

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)
