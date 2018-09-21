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
        workshopName = handler_input.request_envelope.request.intent.slots["WorkshopName"].value

        speech = {
            "photoshop"         : "Our photoshop workshop will walk you through the basics and how to start designing in photoshop.",
            "excel"             : "In this 90 minute hands-on workshop, you will experience the basics of working with Excel including entering text and numbers, using formulas and functions to calculate totals, percentages, and averages, and creating a chart. No prior spreadsheet experience is required.",
            "word"              : "In this 90 minute hands-on workshop, you will be introduced to the essential elements of Microsoft Word. Upon completion, you will be able to insert, delete, select, move and copy text; apply and change formats; control page breaks and use tables to organize information. You will be able to create a header and footer to repeat information on each page automatically. You will insert a photo, change margins and explore print options. Keyboard shortcuts and right-mouse shortcut menus will be included. No prior Word experience is required, though some experience will provide the most beneficial learning experience.",
            "powerpoint"        : "In this 90 minute hands-on workshop, you will be introduced to PowerPoint by creating a presentation with formatted text and graphics. You will use PowerPoint views to organize, rearrange and display your presentation. No prior PowerPoint experience is required.",
            "3d printing"       : "In this 90 minute workshop, you will be introduced to the world of three d printing and its application. We'll walk you through how to create simple three d models and how to prepare them for printing.",
            "after effects"     : "placeholder",
            "illustrator"       : "A 90 minute hands on class covering the basic aspects of Adobe Illustrator. Topics covered include basic functionality such as creating and editing paths, objects, outlines, fills, type, bitmap images, and other tools. Additional topics will include design tips and concepts.",
            "indesign"          : "Adobe InDesign is the preferred program for professional quality publications including flyers and information pamphlets. In this 80 minute hands-on workshop you will be introduced to the basic features of Adobe InDesign including page setup, layout, addition of text and graphics, formatting and discussion of printing issues.",
            "premier"           : "In this fun hands-on workshop, you will use Adobe Premiere Pro to import digital video footage, cut segments, edit audio, add photos, text, transitions, and effects, as well as rendering and exporting. No prior digital editing experience is necessary.",
            "final cut"         : "A 90 minute hands on introduction to editing video utilizing Final Cu Pro X. This also serves as a basic introduction to video editing in Final Cut Pro X. Skills learned include: capturing video, cutting video, adding effects, transitions, titles, and basic video conversions (encoding).",
            "imovie"            : "In this fun hands-on workshop, you will create your first video with easy to use iMovie. You will capture digital video footage, cut segments, add photos, text and transitions. Considerations for recording and playback will be discussed. No prior digital editing experience is necessary",
            "arduino"           : "In this workshop, we'll introduce you to the arduino, a small micro controller that's capable of a lot!",
            "audacity"          : "In this workshop, we'll cover how to use audacity, a free audio editing program.",
            "home automation"   : "placeholder",
            "raspberry pi"      : "placeholder",
            "lightroom"         : "placeholder",
            "vr"                : "This 15 - 20 minute workshop is intended to show students the procedures for operating our VR equipment along with a brief overview of how some of the hardware features function. Completing this workshop is necessary to be able to use the Vive room.",
            "wordpress"         : "Create your site or blog using WordPress. Customize it with themes, photos, movies, text, and widgets."
        }.get(workshopName, "Sorry, I can't find that workshop")

        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

class FullWorkshopListIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("FullWorkshopListIntent")(handler_input)
    
    def handle(self, handler_input):
        speech = """The workshops we teach are three d printing and making, adobe after effects, 
            Adobe Illustrator, Adobe InDesign, Adobe Photoshop, Adobe Premiere Pro, Apple Final Cut, 
            Apple iMovie, Arduino, Audacity, Home Automation, Raspberry Pi, Lightroom, Microsoft Excel, 
            Microsoft Publisher, Microsoft Word, Virtual Reality, and Wordpress."""

        handler_input.response_builder.speak(speech)
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
