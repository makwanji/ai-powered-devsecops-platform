import os
from ollama import chat

from tools.kubernetes import (
    get_pods,
    get_deployments,
    get_services,
    get_events,
    describe_pod,
    get_logs,
)


MODEL = os.getenv("OLLAMA_MODEL", "qwen3-coder")


SYSTEM_PROMPT = """
You are a Kubernetes Troubleshooting Agent.

Your job is to investigate Kubernetes problems and explain the
root cause to the user.

You have access to READ-ONLY Kubernetes tools.

Available tools:

- get_pods
- get_deployments
- get_services
- get_events
- describe_pod
- get_logs

IMPORTANT SAFETY RULES:

You MUST NOT modify the Kubernetes cluster.

Never:
- delete resources
- apply manifests
- create resources
- patch resources
- restart workloads
- scale deployments
- execute commands inside containers

You may ONLY inspect Kubernetes resources.

TROUBLESHOOTING METHOD:

1. Understand the user's problem.
2. Gather evidence using Kubernetes tools.
3. Check pod status.
4. Check deployment status.
5. Check events when appropriate.
6. Check pod details when appropriate.
7. Check logs when appropriate.
8. Correlate the evidence.
9. Identify the most likely root cause.
10. Explain the evidence.
11. Recommend remediation.

Do NOT guess.

If there is insufficient information, gather more information using
the available tools.

When finished, provide:

Root Cause:
<root cause>

Evidence:
<important evidence>

Recommended Fix:
<recommended action>

IMPORTANT:
Do not execute the recommended fix.
Only explain what should be done.
"""


TOOLS = [
    get_pods,
    get_deployments,
    get_services,
    get_events,
    describe_pod,
    get_logs,
]


def run_agent(user_message: str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    max_iterations = 10

    for _ in range(max_iterations):

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        messages.append(response.message)

        tool_calls = response.message.tool_calls

        if not tool_calls:
            return response.message.content

        for tool_call in tool_calls:

            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(
                f"Agent tool call: "
                f"{function_name}({arguments})"
            )

            tool_map = {
                "get_pods": get_pods,
                "get_deployments": get_deployments,
                "get_services": get_services,
                "get_events": get_events,
                "describe_pod": describe_pod,
                "get_logs": get_logs,
            }

            function = tool_map.get(function_name)

            if function is None:
                result = f"ERROR: Unknown tool {function_name}"

            else:
                try:
                    result = function(**arguments)
                except Exception as exc:
                    result = f"ERROR executing tool: {exc}"

            messages.append(
                {
                    "role": "tool",
                    "content": result,
                }
            )

    return "Agent stopped because the maximum number of tool iterations was reached."
