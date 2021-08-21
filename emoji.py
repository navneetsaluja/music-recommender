import emot
emot_obj = emot.core.emot()

import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

def mean_check(mean):
    try:
        mean_text = mean[0].lower()
        print(mean_text)
        mood = "noemo" 
        happy = ["happ", "joy", "laugh", "grin", "excite","smile"]
        sad = ["sad", "frown", "cry", "dismay"]
        anger = ["shame", "angry", "annoy"]
        surprise = ["surprise", "amaze", "astonish", "shock"]
        disgust = ["vomit", "disgust", "nausea", "confound"]
        fear = ["fear", "scare"]
        if any(x in mean_text for x in happy):
            mood = "happy"
        elif any(x in mean_text for x in sad):
            mood = "sad"
        elif any(x in mean_text for x in anger):
            mood = "anger"
        elif any(x in mean_text for x in surprise):
            mood = "surprise"
        elif any(x in mean_text for x in disgust):
            mood = "disgust"
        elif any(x in mean_text for x in fear):
            mood = "fear"
        else:
            mood = "noemo"
        
        return mood
    
    except IndexError:
        return "noemo"

def emoji_check(text):
    if(emot_obj.emoji(text)['flag']):
        l = emot_obj.emoji(text)['value']
        common = max(set(l), key=l.count)
        return mean_check(emot_obj.emoji(common)['mean'])
    elif(emot_obj.emoticons(text)['flag']):
        l = emot_obj.emoticons(text)['value']
        common = max(set(l), key=l.count)
        return mean_check(emot_obj.emoticons(common)['mean'])
    else:
        return "noemo"

class EmojiAnalyzer(Component):
    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        return []

    defaults = {}
    supported_language_list = None
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(EmojiAnalyzer, self).__init__(component_config)

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
                  "entity": "emoji",
                  "extractor": "emoji_extractor"}

        return entity

    def process(self, message: Message, **kwargs: Any) -> None:

        try:
            message.data['text']
            res = emoji_check(message.data['text'])
            entity = self.convert_to_rasa(res, 1)

            message.set("emoji", [entity], add_to_output=True)

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
