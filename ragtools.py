import re
from typing import Any

from rtmt import RTMiddleTier, Tool, ToolResult, ToolResultDirection

_refer_to_medical_database_tool_schema = {
    "type": "function",
    "name": "referToMedicalDatabase",
    "description": "You can call this function to get the refer to medical database when asked for appointment, prescription lab results.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_query": {
                "type": "string",
                "description": "User query to refer to medical database"
            }
        },
        "required": ["user_query"],
        "additionalProperties": False
    }
}

async def _refer_to_medical_database_tool(args: Any) -> ToolResult:
    print(f"Searching for '{args['user_query']}' in the knowledge base.")
    user_query = args["user_query"]

    result =  "Please call back after some time"

    print(f'Referring to medical database for: {user_query}')

    if re.search(r'appointment', user_query, re.IGNORECASE):
        result = "You have an appointment with Dr. Smith on 12th August 2021 at 10:00 AM"
    if re.search(r'prescription', user_query, re.IGNORECASE):
        result = "You have a prescription for 5mg of Lisinopril"
    if re.search(r'lab results', user_query, re.IGNORECASE):
        result =  "Your lab results are normal"

    return ToolResult(result, ToolResultDirection.TO_SERVER)


def attach_rag_tools(rtmt: RTMiddleTier) -> None:
    rtmt.tools["referToMedicalDatabase"] = Tool(schema=_refer_to_medical_database_tool_schema, target=lambda args: _refer_to_medical_database_tool(args))
