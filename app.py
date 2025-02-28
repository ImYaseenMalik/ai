import requests
from transformers import pipeline
import streamlit as st

# Web search function
def search_web(query):
    api_key = "2b2f6b9d80cf773e895f58831f3bd888df4f0a38d522d5d9f52ca16b44b68080"  # Your SerpAPI key
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("organic_results", [])
    else:
        return []

# AI answer function
def ai_answer(query, web_results):
    if not web_results:
        return "I couldn’t find anything—try another question!"
    
    text_to_summarize = " ".join([r["snippet"] for r in web_results[:3]])
    if not text_to_summarize:
        return "Not enough info—rephrase it maybe?"
    
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    summary = summarizer(text_to_summarize, max_length=50, min_length=20, do_sample=False)
    return summary[0]["summary_text"]

# Streamlit interface
st.title("AI Web Search Chat")
st.write("Ask me anything, and I’ll find an answer from the web!")
user_input = st.text_input("Your question:", "")
if user_input:
    with st.spinner("Thinking..."):
        results = search_web(user_input)
        answer = ai_answer(user_input, results)
    st.write(f"**Answer:** {answer}")