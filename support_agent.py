from typing_extensions import TypedDict, Annotated

from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain_community.tools import tool
from langchain_core.messages import HumanMessage, AnyMessage

from langchain_community.utilities import SerpAPIWrapper
from langchain_tavily import TavilySearch
from langchain_community.tools import DuckDuckGoSearchResults

from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


llm = init_chat_model("gpt-4.1", temperature=0.7)

serpapi_tool = Tool(
    name="serpapi",
    description="Searches the web for device fixes, step-by-step troubleshooting, and the latest user reports or guides.",
    func=SerpAPIWrapper().run,
)

duckduckgo_tool = Tool(
    name="duckduckgo_search",
    description="Finds troubleshooting articles, official fixes, and forum discussions about device issues.",
    func=DuckDuckGoSearchResults().run,
)

tavily_tool = Tool(
    name="tavily_search",
    description="Performs web searches for tech support guides, bug reports, and step-by-step device solutions in real time.",
    func=TavilySearch().run,
)


# Create the list of properly wrapped Tool instances
tools = [serpapi_tool, duckduckgo_tool, tavily_tool]

react_prompt = """
You are an expert AI tech support agent that helps users troubleshoot device and software problems.

You have access to the following tools:
- WebSearch (SerpAPI, DuckDuckGo, or Tavily): Search the web, forums, and news for real-time device fixes, step-by-step troubleshooting, bug reports, and official support articles.
- TutorialGenerator: Generate or retrieve step-by-step guides for resolving technical issues (such as clearing cache, resetting network, etc).
- ForumSearch: Look up discussions and common issues on support forums.

For every user request:
1. **Understand** the user’s problem and any device or app specifics.
2. **Break the problem down** into smaller tasks if needed, thinking out loud at each step (“Thought:”).
3. For each subtask, **choose and use the appropriate tool**:
    - Format each action as:  
      Thought: Your reasoning  
      Action: Tool name (WebSearch, TutorialGenerator, ForumSearch, etc)  
      Action Input: Precise input for the tool  
      Observation: The tool’s actual output
4. If any tool or search returns no results, try an alternative site, approach, or suggest what the user might do next.
5. After all necessary steps are done, **ALWAYS output your answer in one final message starting with 'Final answer:'**  
    - Summarize findings, extracted fixes, or step-by-step instructions.
    - Highlight any recurring issues or relevant advice.
    - Suggest next steps or further troubleshooting if needed.

IMPORTANT:  
- Do not output any message starting with "Final answer:" until you are genuinely finished.
- Your last message must **always begin with 'Final answer:'**.

---
Example user request:
"My iPhone battery drains quickly after the latest update. What are common fixes? Also, guide me through clearing cache, and check if there are reports of battery issues on Apple’s forums."

Your reply should use the format above, reason out loud with Thought/Action/Observation steps for each part, and finish ONLY with a message like:

Final answer:  
[List of recommended fixes, step-by-step cache clearing, and summary of forum findings for battery issues.]
"""



class State(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]

def reasoning_node(state: State):
    # LLM with bound tools to enable tool-calling
    llm_with_tools = llm.bind_tools(tools)
    messages = [{"role": "system", "content": react_prompt}] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": state["messages"] + [response]}


tool_node = ToolNode(tools = tools)


def should_continue(state: State):
    last_message = state["messages"][-1]
    if hasattr(last_message, "content") and "final answer:" in last_message.content.lower():
        return "end"
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    if len(state["messages"]) > 20:
        return "end"
    # Otherwise, no tool_calls, not a final answer, so end gracefully
    return "end"


builder = StateGraph(State)
builder.add_node("reason", reasoning_node)
builder.add_node("action", tool_node)
builder.set_entry_point("reason")
builder.add_conditional_edges(
    "reason",
    should_continue,
    {
        "continue": "action",
        "end": END,
    }
)
builder.add_edge("action", "reason")
support_agent = builder.compile()
