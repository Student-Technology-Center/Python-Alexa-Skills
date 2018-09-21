
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import AbstractRequestHandler

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        speech = "This is a test!"
        print("Alexa Request: {}\n".format(handler_input.request_envelope.request))
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class HelloRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("HelloIntent")(handler_input)
    
    def handle(self, handler_input):
        speech = "Hello!"
        print("Alexa Request: {}\n".format(handler_input.request_envelope.request))
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(HelloRequestHandler())

lambda_handler = sb.lambda_handler()
