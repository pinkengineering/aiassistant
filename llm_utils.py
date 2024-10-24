def query_llm(bedrock, messages, tools, system_prompt):
    """Make a request to the LLM and return the response."""
    return bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=messages,
        inferenceConfig={"maxTokens": 2000, "temperature": 0},
        toolConfig={"tools": tools},
        system=[{"text": system_prompt}],
    )