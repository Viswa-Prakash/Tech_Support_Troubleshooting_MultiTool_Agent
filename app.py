import streamlit as st
from langchain_core.messages import HumanMessage
from support_agent import support_agent

# Tech Support Troubleshooting Multi Tool Agent
st.set_page_config(page_title="Tech Support Troubleshooting Multi Tool Agent", page_icon=":robot:")

st.title("Tech Support Troubleshooting Multi Tool Agent")

st.markdown("""
            My iPhone battery drains quickly after the latest update. 
            What are common fixes? 
            Also, guide me through clearing cache, 
            and check if there are reports of battery issues on Apple’s forums.
""")

with st.form("query_form"):
    user_query = st.text_area("Enter your query here:", height=60)
    submitted = st.form_submit_button("Ask Agent")

if submitted and user_query.strip():
    with st.spinner("Agent is analyzing..."):
        output = support_agent.invoke({"messages": [HumanMessage(content=user_query)]})
        # Show **only the last agent message** (the Final Answer)
        final_message = None
        for msg in reversed(output["messages"]):
            content = getattr(msg, "content", "")
            if "final answer" in content.lower():
                final_message = content
                break
        if not final_message:
            # fallback: just show last assistant/system message
            last = output["messages"][-1]
            final_message = getattr(last, "content", str(last))
        st.markdown("**Here’s a clear summary of your requests and answers:**\n\n" + final_message)
