import streamlit as st
from langchain.chains import LLMChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

st.title("Simple Chat App")
st.write("Chat with the AI assistant!")

chat_prompt = ChatPromptTemplate(
    [
        ("system", "You are a smart agent whose job is to analyse each line of a phone conversation and provide sentiment analysis on the same. Only return the number from -1, 0 and 1 and nothing else as per the sentiment."),
        ("human", "{input}")
    ]
)

conversation_chain = LLMChain(llm=llm, prompt=chat_prompt)

user_input = st.text_input("What would you like to ask?")

if user_input:
    response = conversation_chain.run(input=user_input)
    st.write(response)
