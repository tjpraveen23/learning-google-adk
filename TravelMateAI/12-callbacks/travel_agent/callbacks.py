from google.adk.agents.context import Context

'''
Why This Is Useful

At this point, the callbacks are only printing messages. That might seem simple, but these are the exact places 
where production applications implement important cross-cutting concerns:

    before_agent → Authenticate users, check permissions, apply guardrails.
    before_tool → Validate tool arguments, enforce policies, log requests.
    after_tool → Record metrics, audit tool usage, transform results.
    after_agent → Filter sensitive content, log responses, measure end-to-end execution time.
'''
async def before_agent(callback_context: Context):
    print("\n" + "=" * 60)
    print("BEFORE AGENT")
    print("=" * 60)
    print("Agent execution started.")

    # Return None to continue normal execution
    return None


async def after_agent(callback_context: Context):
    print("\n" + "=" * 60)
    print("AFTER AGENT")
    print("=" * 60)
    print("Agent execution completed.")

    return None


async def before_tool(tool, args, tool_context):
    print("\n" + "=" * 60)
    print("BEFORE TOOL")
    print("=" * 60)
    print(f"Tool : {tool.name}")
    print(f"Arguments : {args}")

    return None


async def after_tool(
    tool,
    args,
    tool_context,
    tool_response,
):
    print("\n===== AFTER TOOL =====")
    print(f"Tool : {tool.name}")
    print(f"Arguments : {args}")
    print(f"Response : {tool_response}")

    return None