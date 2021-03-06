import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.train import interactive
from rasa_core.utils import EndpointConfig
from rasa_core.policies.fallback import FallbackPolicy

import spacy
from pather import Path
spacy.load('en')

logger = logging.getLogger(__name__)


def run_trade_online(interpreter, domain_file=Path.TRADE_DOMAIN.value, training_data_file=Path.STORIES.value):
    fallback = FallbackPolicy(fallback_action_name="action_default_fallback",
                          core_threshold=0.5,
                          nlu_threshold=0.5)
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")						  
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=2), KerasPolicy(max_history=3, epochs=3, batch_size=50),fallback],
                  interpreter=interpreter,
				  action_endpoint=action_endpoint)
    				  
    data = agent.load_data(training_data_file)			   
    agent.train(data)
    interactive.run_interactive_learning(agent, training_data_file)
    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter(Path.TRADE_NLU_FILE.value)
    run_trade_online(nlu_interpreter)

