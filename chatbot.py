import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

print("HY! How are you?")

while True:
    message = input("you: ")
    if message.lower() == "exit":
        break
    try:
         search = tavily_client.search(
            query=message,search_depth="advanced",
            max_results=5
        )
         web_results = ""
         for result in search["results"]:
           web_results += (
            f"Title: {result['title']}\n"
            f"Content: {result['content']}\n"
            )
      
         response = groq_client.chat.completions.create(
          model="openai/gpt-oss-20b",
           messages=[
               {"role": "system", "content": "You are a helpful AI assistant."},
               {"role": "user", "content": f"User question: {message}\n\n Latest web search results: \n{web_results}"}
           ]
         )
         print("AI Chatbot:", response.choices[0].message.content)
    except Exception as e:
         print("Error:", e)
        
