import json
from aws_clients import initialize_clients
from tools import get_tool_list
from llm_utils import query_llm
from llm_response_processor import process_llm_response

def main():
    # Initialize the AWS clients
    bedrock, lambda_client, s3 = initialize_clients()

    # Get the tool list
    tool_list = get_tool_list()

    # Initialize the message list for the conversation
    message_list = [
        {
            "role": "user",
            "content": [{"text": "I want to escalate this issue."}],
        }
    ]

    # Set the system prompt
    system_prompt = (
        "You are an AI assistant capable of creating Lambda functions, "
        "performing mathematical calculations, and sending emails. "
        "Use the provided tools when necessary."
    )

    # Make the initial request to the LLM
    response = query_llm(bedrock, message_list, tool_list, system_prompt)
    response_message = response["output"]["message"]
    print("Initial response:")
    print(json.dumps(response_message, indent=4))
    message_list.append(response_message)

    # Process the LLM's response
    follow_up_content_blocks = process_llm_response(response_message, lambda_client, s3)

    # If there are follow-up content blocks, make another request to the LLM
    if follow_up_content_blocks:
        follow_up_message = {
            "role": "user",
            "content": follow_up_content_blocks,
        }
        message_list.append(follow_up_message)

        print("Follow-up message:")
        print(json.dumps(follow_up_message, indent=4))

        response = query_llm(bedrock, message_list, tool_list, system_prompt)
        response_message = response["output"]["message"]
        print("Follow-up response:")
        print(json.dumps(response_message, indent=4))
        message_list.append(response_message)

        # Process the final response
        process_llm_response(response_message, lambda_client, s3)

if __name__ == "__main__":
    main()
