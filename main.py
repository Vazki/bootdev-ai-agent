import os
import time
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

def main():
    client = genai.Client(api_key=api_key)

    max_retries = 5
    base_delay = 1  # seconds

    parser = argparse.ArgumentParser(description="Gemini Chatbot")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")    

    args = parser.parse_args()
    prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(20):  # Allow up to 20 interactions in a single session
        if _ == 19:
            print("The model did not produce a final response after 20 interactions. This may indicate an issue with the model or the prompts being used. Please review the conversation history and try again.")
            exit(1)
        function_responses = [] # Reset function responses for each iteration to avoid accumulating them across iterations
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(system_instruction=system_prompt, 
                                                    tools=[available_functions],
                                                    temperature=0)
                )
                if not response.usage_metadata:
                    raise RuntimeError("Response metadata is missing. Cannot determine token usage.")
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
                # After each call to generate_content, check the .candidates property of the response.
                # If there are any "candidates" (there should be), iterate over them and append the .content property of each to the messages list.
                if response.candidates:
                    for candidate in response.candidates:
                        if candidate.content:
                            messages.append(candidate.content)
                if args.verbose:
                    print(
                        f"User prompt: {prompt}\n"
                        f"Prompt tokens: {prompt_tokens}\n"
                        f"Response tokens: {response_tokens}\n"
                    )
                if response.function_calls:
                    for call in response.function_calls:
                        function_call_result = call_function(call, verbose=args.verbose)
                        if function_call_result.parts == []:
                            raise Exception(
                                f"Function call {call.name} did not return any parts. Response: {response}"
                            )
                        if function_call_result.parts[0].function_response is None:
                            raise Exception(
                                f"Function call {call.name} did not return a function response. Response: {response}"
                            )
                        if function_call_result.parts[0].function_response.response is None:
                            raise Exception(
                                f"Function call {call.name} did not return a response in the function response. Response: {response}"
                            )
                        function_responses.append(function_call_result.parts[0])
                        if args.verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                    messages.append(types.Content(role="user", parts=function_responses))
                else:
                    print(response.text)
                    return  # Exit the loop if there are no function calls, assuming the conversation is complete
            except errors.ServerError as e:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                if args.verbose:
                    print(f"ServerError on attempt {attempt + 1}/{max_retries}: {e}. Retrying in {delay}s...")
                else:
                    print(f"ServerError on attempt {attempt + 1}/{max_retries}: {e}. Retrying...")
                time.sleep(delay)

if __name__ == "__main__":
    main()