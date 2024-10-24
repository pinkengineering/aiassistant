def get_tool_list():
    """Define and return the tool list for the LLM to use."""
    return [
        {
            "toolSpec": {
                "name": "send_email",
                "description": "Send an email using the getEmail Lambda function. No input is required.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "cosine",
                "description": "Calculate the cosine of x.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "x": {
                                "type": "number",
                                "description": "The number to pass to the function.",
                            }
                        },
                        "required": ["x"],
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "create_lambda_function",
                "description": "Create and deploy a Lambda function.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The Python code for the Lambda function.",
                            },
                            "function_name": {
                                "type": "string",
                                "description": "The name of the Lambda function.",
                            },
                            "description": {
                                "type": "string",
                                "description": "A description of the Lambda function.",
                            },
                            "has_external_python_libraries": {
                                "type": "boolean",
                                "description": "Whether the function uses external Python libraries.",
                            },
                            "external_python_libraries": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of external Python libraries to include.",
                            },
                        },
                        "required": [
                            "code",
                            "function_name",
                            "description",
                            "has_external_python_libraries",
                            "external_python_libraries",
                        ],
                    }
                },
            }
        },
    ]