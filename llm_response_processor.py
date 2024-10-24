import json
import math
from lambda_utils import call_lambda_function, create_lambda_function

def process_llm_response(response_message, lambda_client, s3):
    """Process the LLM's response, handling tool usage and text output."""
    response_content_blocks = response_message["content"]
    follow_up_content_blocks = []

    for content_block in response_content_blocks:
        # Process toolUse blocks
        if "toolUse" in content_block:
            tool_use_block = content_block["toolUse"]
            tool_use_name = tool_use_block["name"]
            print(f"Using tool {tool_use_name}")

            result = None
            tool_use_id = tool_use_block["toolUseId"]

            # Handle specific tool use cases
            if tool_use_name == "cosine":
                tool_result_value = math.cos(tool_use_block["input"]["x"])
                result = {"result": tool_result_value}

            elif tool_use_name == "send_email":
                lambda_response = call_lambda_function(lambda_client, "getEmail", {})
                print(f"Lambda response: {lambda_response}")

                # Decode the JSON body if it is double-escaped.
                if "body" in lambda_response and isinstance(lambda_response["body"], str):
                    try:
                        # First decode attempt
                        decoded_body = json.loads(lambda_response["body"])

                        # If the result is still a string, attempt decoding again
                        if isinstance(decoded_body, str):
                            decoded_body = json.loads(decoded_body)

                        lambda_response["body"] = decoded_body
                    except json.JSONDecodeError:
                        print("Failed to decode the body content.")
                        lambda_response["body"] = {"error": "Failed to parse response body"}

                result = lambda_response

            elif tool_use_name == "create_lambda_function":
                result = create_lambda_function(
                    lambda_client,
                    s3,
                    tool_use_block["input"]["code"],
                    tool_use_block["input"]["function_name"],
                    tool_use_block["input"]["description"],
                    tool_use_block["input"]["has_external_python_libraries"],
                    tool_use_block["input"]["external_python_libraries"],
                )
                print(f"Lambda function creation result: {result}")

            # Add a toolResult only if a tool was actually used and a result exists
            if result is not None:
                follow_up_content_blocks.append(
                    {
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": result}],
                        }
                    }
                )

    return follow_up_content_blocks
