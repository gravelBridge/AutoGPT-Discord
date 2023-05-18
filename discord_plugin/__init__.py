"""This is the AutoGPT Discord Plugin."""
from typing import Any, Dict, List, Optional, Tuple, TypeVar
from colorama import Fore
from auto_gpt_plugin_template import AutoGPTPluginTemplate

from .discord_plugin import required_info_set, run_bot, wait_for_user_input, commandUnauthorized, Message, messagesToSend, userReply, waitingForReply, finishedLoggingIn
import threading
import time
import os

PromptGenerator = TypeVar("PromptGenerator")

authedCommand = ""

class AutoGPTDiscord(AutoGPTPluginTemplate):
    """
    This the AutoGPT Discord Plugin..
    """

    def __init__(self):
        super().__init__()
        self._name = "AutoGPTDiscord"
        self._version = "0.1.1"
        self._description = "AutoGPT Discord Plugin: Interact with AutoGPT through discord."

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.

        Returns:
            bool: True if the plugin can handle the on_response method."""
        return True

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        
        messagesToSend.append(Message(role="ON_RESPONSE", content=response))
        return response

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.

        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True
    
    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        global askForUserInput
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.

        Args:
            prompt (PromptGenerator): The prompt generator.

        Returns:
            PromptGenerator: The prompt generator.
        """
        if required_info_set():
            print(
                Fore.GREEN
                + f"{self._name} - {self._version} - Discord plugin loaded!"
            )
            try:
                if os.getenv("ASK_FOR_INPUT") == "True":
                    askForUserInput = True
                    prompt.add_command("command_denied", "If you are told to run this command, or this command has been run, then the user has denied your request to run your command. Do not attempt to run the same command again.", {}, commandUnauthorized)
                else:
                    askForUserInput = False

            except:
                print(
                    Fore.RED + "You did not set the ASK_FOR_INPUT env variable correctly. It must be either True or False"
                )
                os._exit(1)

            t = threading.Thread(target = run_bot)
            t.start()
            while True:
                time.sleep(1)
                if finishedLoggingIn[0]:
                    break
            
        else:
            print(
                Fore.RED
                + f"{self._name} - {self._version} - Discord plugin not loaded, because not all the environmental variables were set in the env configuration file."
            )

        messagesToSend.append(Message(role="ON_BOOT", content=""))

        return prompt
    


    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.

        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.

        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.

        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """

        messagesToSend.append(Message(role="POST_PLANNING", content=response))
        return response

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.

        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.

        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            Optional[str]: The resulting message.
        """
        pass

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.

        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return True

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        
        messagesToSend.append(Message(role="POST_INSTRUCTION", content=response))
        return response


    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.

        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return askForUserInput

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.

        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.

        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        global authedCommand
        if askForUserInput:
            if command_name != authedCommand:
                authedCommand = ""
                input = wait_for_user_input(command_name, arguments)
                if input == "Authorized":
                    authedCommand = command_name
                    return (command_name, arguments)
                elif input == "Unauthorized":
                    return ("command_denied", {"feedback": "The command was denied, try something else."})
                else:
                    return ("command_denied", {"feedback": input})
            else:
                return (command_name, arguments)
        else:
            return (command_name, arguments)

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.

        Returns:
            bool: True if the plugin can handle the post_command method."""
        return True

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.

        Args:
            command_name (str): The command name.
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        
        messagesToSend.append(Message(role="POST_COMMAND", content=response))
        return response

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

        Returns:
            str: The resulting response.
        """
        pass

    def can_handle_text_embedding(
        self, text: str
    ) -> bool:
        """This method is called to check that the plugin can
          handle the text_embedding method.
        Args:
            text (str): The text to be convert to embedding.
          Returns:
              bool: True if the plugin can handle the text_embedding method."""
        return False
    
    def handle_text_embedding(
        self, text: str
    ) -> list:
        """This method is called when the chat completion is done.
        Args:
            text (str): The text to be convert to embedding.
        Returns:
            list: The text embedding.
        """
        pass

    def can_handle_user_input(self, user_input: str) -> bool:
        """This method is called to check that the plugin can
        handle the user_input method.

        Args:
            user_input (str): The user input.

        Returns:
            bool: True if the plugin can handle the user_input method."""
        return True

    def user_input(self, user_input: str) -> str:
        """This method is called to request user input to the user.

        Args:
            user_input (str): The question or prompt to ask the user.

        Returns:
            str: The user input.
        """

        print("user input function called")
        messagesToSend.append(Message(role="REQUEST_INPUT", content=user_input))
        waitingForReply[0] = True

        while(len(userReply) == 0):
            time.sleep(1)

        return userReply.pop(0)
    
    def can_handle_report(self) -> bool:
        """This method is called to check that the plugin can
        handle the report method.

        Returns:
            bool: True if the plugin can handle the report method."""
        return True



    def report(self, message: str) -> None:
        """This method is called to report a message to the user.

        Args:
            message (str): The message to report.
        """
        messagesToSend.append(Message(role="REPORT", content=message))

