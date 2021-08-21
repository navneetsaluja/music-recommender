import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

def final_check(emoji, synonym, sentiment, model):
    if emoji != "noemo":
        res = emoji
    else:
        if synonym != "none":
            res = synonym
        else:
            if (sentiment == "pos"):
                if (model in ("joy", "surprise")):
                    res = model
                else: 
                    res = "happy"
            elif (sentiment == "neg"):
                if (model in ("sad", "disgust", "fear", "anger")):
                    res = model
                else:
                    res = "sad"
            elif (sentiment == "neu"):
                res = "noemo"
            
            else:
                res = "noemo"
    
    return res
                


class FinalChecker(Component):
    defaults = {}
    supported_language_list = None
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(FinalChecker, self).__init__(component_config)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        pass

    def convert_to_rasa(self, value, confidence):
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "final_emotion",
                  "extractor": "final_extractor"}

        return entity

    def process(self, message: Message, **kwargs: Any) -> None:
        try:
            message.data['text']
            earlier_value = 'noemo'

            with open('file.txt') as f:
                for line in f:
                    earlier_value = line
            f = open('file.txt', 'w')

            emoji = message.data['emoji'][0]['value']
            synonym = message.data['synonym'][0]['value']
            sentiment  = message.data['sentiment'][0]['value']
            model = message.data['model'][0]['value']
            res = final_check(emoji, synonym, sentiment, model)
            if (earlier_value != 'noemo' and res == 'noemo'):
                entity = self.convert_to_rasa(earlier_value, 1)
                f.write(earlier_value)
            else: 
                entity = self.convert_to_rasa(res, 1)
                f.write(res)

            message.set("entities", [entity], add_to_output=True)
            f.close()
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
