import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful and friedly AI Assistent. Your role is to help users with their questions clearly and simple language. Maintain context frim previous conversation."""

st.set_page_config(page_title="AI Chatbot")
st.title("AI Intern - Smart Chatbot")

# Clients with error handling
try:

    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
except Exception as e:
    st.error(f"API KEY ERROR: {e}")

# Conversation History / Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat Feature
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Sidebar Deliverables
st.sidebar.markdown("Deliverables Done:")
st.sidebar.write("✅ User Input")
st.sidebar.write("✅ AI Response")
st.sidebar.write("✅ Loading State")
st.sidebar.write("✅ Error Handling")
st.sidebar.write("✅ Clean Interface")
st.sidebar.write("✅ System Prompt")
st.sidebar.write("✅ Conversation History")
st.sidebar.write("✅ Clear Chat")

#Display history with markdown 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input With Validation
if prompt := st.chat_input("Ask  something...."):
    if not prompt.strip():
        st.toast("Please enter a valid message!")
    elif len(prompt) > 1000:
        st.toast("Message too long! Max 1000 chars.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking....."):
                try:
                    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.messages[-10:]:
                        if m.get("role") in ["user", "assistant"]:
                            if m.get("content") and m["content"].strip():
                                api_messages.append({"role": m["role"], "content": m["content"]})
                                

                    completion = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=api_messages
                        )
                    response = completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = (f"Error: {str(e)}. Please check your API Key or internet.")
                    st.markdown(error_msg)
