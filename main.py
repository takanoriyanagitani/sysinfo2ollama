import os
import subprocess

from typing import Any

import ollama

def get_storage_info() -> str:
    """
    Gets storage info.

    Returns:
        str: A string that describes the storage info.
    """

    dfh = ["df", "-h", "."]
    res = subprocess.run(dfh, capture_output=True, text=True)

    return res.stdout

def get_memory_info() -> str:
    """
    Gets memory info.

    Returns:
        str: A string that describes the memory info.
    """

    mp = ["memory_pressure"]
    res = subprocess.run(mp, capture_output=True, text=True)
    return res.stdout

available_tools: dict[str,Any] = dict(
    get_storage_info = get_storage_info,
    get_memory_info = get_memory_info,
)

def chat(
    msgs,
    mname="llama3.2:3b",
    tools=[get_storage_info, get_memory_info],
) -> ollama.ChatResponse:
    return ollama.chat(
        mname,
        msgs,
        tools=tools,
    )

def main():
    modelname: str = os.getenv("ENV_MODEL_NAME") or "llama3.2:3b"

    msg: str = os.getenv("ENV_PROMPT") or "Basic storage/memory health report"

    msgs = [
        dict(role="user", content=msg),
    ]

    res0: ollama.ChatResponse = chat(msgs, mname=modelname)
    calls = res0.message.tool_calls
    if not(calls):
        print("no calls got")
        return

    if 2 != len(calls):
        print("too few calls")
        return

    for tool in calls:
        name: str = tool.function.name
        found = available_tools.get(name)
        if not(found):
            print(f"no such func: {name}")
            return
        args = tool.function.arguments
        output = found(**args)
        msgs.append(dict(
            role = "tool",
            content = str(output),
            tool_name = name,
        ))
        pass

    final = chat(
        msgs,
        mname=modelname,
        tools=[]
    )

    print(final.message.content)
    pass

if __name__ == "__main__":
    main()
