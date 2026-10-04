import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a helpful and friedly AI Assistent. Your role is to help users with their questions clearly and simple language."""

st.set_page_config(page_title="AI Chatbot")
st.title("AI Intern - Smart Chatbot")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("Deliverables Done:")
st.sidebar.write("✅ User Input")
st.sidebar.write("✅ AI Response")
st.sidebar.write("✅ Loading State")
st.sidebar.write("✅ Error Handling")
st.sidebar.write("✅ Clean Interface")
st.sidebar.write("✅ System Prompt")
st.sidebar.write("✅ Conversation History")
st.sidebar.write("✅ Clear Chat")
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask  something...."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
         with st.spinner("Thinking....."):
             try:
                 api_messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                 for m in st.session_state.messages:
                     if m["role"] in ["user", "assistant"]:
                        api_messages.append({"role": m["role"], "content": m["content"]
                         })
                 response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=api_messages
                        )
                 answer = response.choices[0].message.content
                 st.markdown(answer)
                 st.session_state.messages.append({"role": "assistent", "content": answer})
                    
             except Exception as e:
                 st.error(f"Error: {e}. Please check your API Key or internet.")
