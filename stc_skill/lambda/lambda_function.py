from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model import Response

sb = SkillBuilder()

LAUNCH_SPEECH = "Hello, this is the STC! What can I help you with?"

INTENT_DICT = {}


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        print("Alexa Request: {}\n".format(handler_input.request_envelope.request))

        handler_input.response_builder.speak(LAUNCH_SPEECH).ask(LAUNCH_SPEECH)
        return handler_input.response_builder.response

class SessionEndRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input) or is_intent_name("AMAZON.CancelIntent")(handler_input)
    
    def handle(self, handler_input):
        handler_input.response_builder.speak("Okay, bye.")
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        print("Alexa Request: {}\n".format(handler_input.request_envelope.request))
        speech = "I can give you info on the STC or our upcoming workshops. Would you like help with either?"

        handler_input.response_builder.speak(speech).ask(speech)
        handler_input.attributes_manager.session_attributes["YES_NO_RETURN"] = "AMAZON.HelpIntent"

        return handler_input.response_builder.response
    
    def handle_yes(self, handler_input):
        speech = "Great, would you like info on the STC or the workshops?"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
    
    def handle_no(self, handler_input):
        handler_input.response_builder.speak("Okay, just ask if you need help!")
        return handler_input.response_builder.response

class STCInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("STCInfoIntent")(handler_input)
    
    def handle(self, handler_input):
        handler_input.response_builder.speak(
            """The Student Technology Center supports the 
            advancement of student knowledge of technology from fundamental 
            skills to advanced applications. The STC is a place where 
            students attend workshops, schedule peer tutoring, and make use 
            of manuals, tutorials and other advanced equipment and software 
            to promote their learning."""
        )
        return handler_input.response_builder.response

class STCWorkshopInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("STCWorkshopInfoIntent")(handler_input)
    
    def handle(self,  handler_input):
        speech = """We teach a variety of workshops such as Photoshop, "
            Microsoft Excel, three d printing and more. Would you "
            like more info on a workshop or would like to hear "
            the full list?"""

        handler_input.response_builder.speak(speech).ask(speech)
        handler_input.attributes_manager.session_attributes["YES_NO_RETURN"] = "STCWorkshopInfoIntent"

        return handler_input.response_builder.response
    
    def handle_yes(self, handler_input):
        speech = "Okay. Would you like more info on a workshop or hear a full list?"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response
    
    def handle_no(self, handler_input):
        handler_input.response_builder.speak("Okay, no worries")

        return handler_input.response_builder.response

class SpecificWorkshopInfoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SpecificWorkshopIntent")(handler_input)
    
    def handle(self, handler_input):
        handler_input.response_builder.speak("This is a placeholder for specific workshop intent")
        return handler_input.response_builder.response

class FullWorkshopListIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("FullWorkshopListIntent")(handler_input)
    
    def handle(self, handler_input):
        handler_input.response_builder.speak("This is a placeholder for Full Workshop List Intent")
        return handler_input.response_builder.response

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("YesIntent")(handler_input)
    
    def handle(self, handler_input):
        intentHandler = handler_input.attributes_manager.session_attributes["YES_NO_RETURN"]
        handler_input.attributes_manager.session_attributes["YES_NO_RETURN"] = ""

        if intentHandler == "AMAZON.HelpIntent":
            return HelpIntentHandler().handle_yes(handler_input)
        elif intentHandler == "STCWorkshopInfoIntent":
            return STCWorkshopInfoIntentHandler().handle_yes(handler_input)
        else:
            handler_input.response_builder.speak("Yes to what?")
            return handler_input.response_builder.response

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NoIntent")(handler_input)
    
    def handle(self, handler_input):
        intentHandler = handler_input.attributes_manager.session_attributes["YES_NO_RETURN"]
        handler_input.attributes_manager.session_attributes["YES_NO_RETURN"] = ""

        if intentHandler == "AMAZON.HelpIntent":
            return HelpIntentHandler().handle_no(handler_input)
        elif intentHandler == "STCWorkshopInfoIntent":
            return STCWorkshopInfoIntentHandler().handle_no(handler_input)
        else:
            handler_input.response_builder.speak("No to what?")
            return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print("Encountered following exception: {}".format(exception))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SessionEndRequestHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(STCInfoIntentHandler())
sb.add_request_handler(STCWorkshopInfoIntentHandler())
sb.add_request_handler(FullWorkshopListIntentHandler())
sb.add_request_handler(SpecificWorkshopInfoIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
