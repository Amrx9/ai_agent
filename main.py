import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple

from prompts import SYSTEM_PROMPT
from functions.function_registry import get_available_functions, execute_function


def parse_command_line_args(args: List[str]) -> Tuple[bool, List[str]]:
    """Parse command line arguments into verbose flag and user arguments."""
    verbose = "--verbose" in args
    user_args = [arg for arg in args if not arg.startswith("--")]
    return verbose, user_args


def validate_user_input(user_args: List[str]) -> Optional[str]:
    """Validate user input and return error message if invalid."""
    if not user_args:
        return ("AI Code Assistant\n"
                'Usage: python main.py "your prompt here" [--verbose]\n'
                'Example: python main.py "How do I build a calculator app?"')
    return None


def create_initial_message(user_prompt: str) -> List[types.Content]:
    """Create the initial message list with user prompt."""
    return [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]


def create_client(api_key: str) -> genai.Client:
    """Create and return a Gemini API client."""
    return genai.Client(api_key=api_key)


def generate_response(client: genai.Client, messages: List[types.Content], 
                     available_functions: types.Tool, verbose: bool) -> types.GenerateContentResponse:
    """Generate content using the Gemini API."""
    return client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=SYSTEM_PROMPT
        )
    )


def log_token_usage(response: types.GenerateContentResponse, verbose: bool) -> None:
    """Log token usage if verbose mode is enabled."""
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def extract_function_calls(response: types.GenerateContentResponse) -> List[Any]:
    """Extract function calls from the API response."""
    return response.function_calls or []


def process_function_calls(function_calls: List[Any], verbose: bool) -> List[types.Part]:
    """Process all function calls and return their responses."""
    return [
        execute_function(func_call, verbose)
        for func_call in function_calls
    ]


def update_messages_with_response(messages: List[types.Content], 
                                response: types.GenerateContentResponse) -> List[types.Content]:
    """Add the assistant's response to the message history."""
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    return messages


def update_messages_with_tool_responses(messages: List[types.Content], 
                                      tool_responses: List[types.Part]) -> List[types.Content]:
    """Add tool responses to the message history."""
    if tool_responses:
        messages.append(types.Content(role="tool", parts=tool_responses))
    return messages


def extract_text_response(response: types.GenerateContentResponse) -> Optional[str]:
    """Extract text response from the API response."""
    if response.candidates:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'text') and part.text:
                    return part.text
    return None


def conversation_loop(client: genai.Client, messages: List[types.Content], 
                     available_functions: types.Tool, verbose: bool) -> Optional[str]:
    """Main conversation loop that handles the back-and-forth with the AI."""
    max_iterations = 20
    
    for iteration in range(max_iterations):
        try:
            # Generate response
            response = generate_response(client, messages, available_functions, verbose)
            log_token_usage(response, verbose)
            
            # Update messages with assistant response
            messages = update_messages_with_response(messages, response)
            
            # Check for function calls
            function_calls = extract_function_calls(response)
            
            if function_calls:
                # Process function calls
                tool_responses = process_function_calls(function_calls, verbose)
                messages = update_messages_with_tool_responses(messages, tool_responses)
            else:
                # No function calls, check for final text response
                text_response = extract_text_response(response)
                if text_response:
                    return text_response
                
        except Exception as e:
            print(f"Error in iteration {iteration + 1}: {e}")
            return None
    
    print(f"Maximum iterations ({max_iterations}) reached.")
    return None


def main() -> None:
    """Main entry point of the application."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    verbose, user_args = parse_command_line_args(sys.argv[1:])
    
    # Validate input
    error_message = validate_user_input(user_args)
    if error_message:
        print(error_message)
        sys.exit(1)
    
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not found")
        sys.exit(1)
    
    # Create client and prepare for conversation
    client = create_client(api_key)
    user_prompt = " ".join(user_args)
    messages = create_initial_message(user_prompt)
    available_functions = get_available_functions()
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    
    # Run conversation loop
    final_response = conversation_loop(client, messages, available_functions, verbose)
    
    if final_response:
        print("Final response:")
        print(final_response)
    else:
        print("No final response received.")


if __name__ == "__main__":
    main()