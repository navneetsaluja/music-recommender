import typing
from typing import Any, Optional, Text, Dict, List, Type

import numpy as np, pandas as pd
from numpy.random import RandomState
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pickle

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

def mod_check(text):
    filename = 'finalized_model.pkl'

    df3 = pd.read_csv('df3.csv', converters={'emotions': eval})

    rng = RandomState()

    train = df3.sample(frac=0.7, random_state=rng)
    test = df3.loc[~df3.index.isin(train.index)]

    X_train, X_test, y_train, y_test = train_test_split(df3['text'].values.astype('U'), df3['final_cat'].values.astype('U'), random_state=1)

    cv = CountVectorizer(strip_accents='ascii', lowercase=True, stop_words='english')
    X_train_cv = cv.fit_transform(X_train)

    loaded_model = pickle.load(open(filename, 'rb'))
    li = [text]
    array = np.array((li))
    array_cv = cv.transform(array)
    return (loaded_model.predict(array_cv)[0])


class ModelComponent(Component):

    defaults = {}
    supported_language_list = None
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super(ModelComponent,self).__init__(component_config)

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
            w = message.data['text']  
            res = mod_check(w)
            entity = self.convert_to_rasa(res, 1)
            message.set("model", [entity], add_to_output=True)
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
