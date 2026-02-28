import os

from argparse import ArgumentParser
from dotenv import load_dotenv
from google import genai
from google.genai import types

from errors.error_handling import error_handler
from functions.call_function import call_function
from prompts import system_prompt
from functions.get_files_info import schema_get_file_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

from config import MAX_MODEL_ITERATIONS

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
parser = ArgumentParser(description="Chatbot")
available_functions = types.Tool(
    function_declarations=[
        schema_get_file_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)


def _process_function_calls(args, response, messages):
    function_calls = response.function_calls
    function_responses = []
    if function_calls is not None:
        for function_call in function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception(
                    f"Error: Function Call failed prematurly {function_call.name}({function_call.args})"
                )

            if not function_call_result.parts[0].function_response:
                raise Exception(
                    f"Error: Function Call failed - function did not respond. \n On:{function_call.name}({function_call.args})"
                )

            if not function_call_result.parts[0].function_response.response:
                raise Exception(
                    f"Error: Function Call Failed - Function Response was not correct. \n On:{function_call.name}({function_call.args})"
                )

            function_responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        # append function_call_result to messages once done.
        messages.append(types.Content(role="user", parts=function_responses))
        return True
    else:
        return False


def _add_message_candidates(messages, response):
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)


def _process_model_output(args, messages, response):
    if response.usage_metadata is None:
        raise RuntimeError(
            "An error occured while trying to call the Gemini API. Please try again or check the logs if the issue persists",
            response,
        )

    # adds model response candidates to messages
    if response.candidates:
        _add_message_candidates(messages, response)

    # Check function calls and process the functions accordingly before appending function result to messages
    # returns a boolean flag indicating whether to continue processing or end loop
    return _process_function_calls(args, response, messages)


def _model_call(messages):
    try:
        return client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[available_functions],
            ),
        )
    except Exception as e:
        error_handler(e)


def _final_message(response, user_prompt, verbose_flag):
    metadata = response.usage_metadata

    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")
    del metadata, user_prompt, verbose_flag, response


def _model_repl():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    responses = []

    for iteration in range(MAX_MODEL_ITERATIONS):
        response = _model_call(messages)
        continue_flag = _process_model_output(args, messages, response)
        if not continue_flag:
            _final_message(response, args.user_prompt, args.verbose_flag)
            break
        elif iteration == MAX_MODEL_ITERATIONS - 1:
            print("Error: Model execution exceeded max iteration limit")
            exit(1)

    del responses, messages, args


def main():
    if api_key is None:
        raise Exception("Api Key not found. Check variables and try again")

    _model_repl()


if __name__ == "__main__":
    main()
