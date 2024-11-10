from langchain.chains import LLMChain
# from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

def sentiment_analysis_chat(input_text):
    # Improved prompt for clearer and more accurate sentiment analysis
    chat_prompt = ChatPromptTemplate(
        [
            ("system", "You are an advanced AI assistant skilled in sentiment analysis. Your task is to analyze the emotional tone of each line in a phone conversation and return a sentiment score as a single number between -1 and 1. Here’s how to interpret the scale:\n\n"
             "-1: Strongly negative\n"
             "-0.5: Moderately negative\n"
             "0: Neutral\n"
             "0.5: Moderately positive\n"
             "1: Strongly positive\n\n"
             "Only return the sentiment score as a number without additional text. Analyze the content carefully to accurately reflect the emotional tone."),
            ("human", "{input}")
        ]
    )

    # Create a conversation chain
    conversation_chain = LLMChain(llm=llm, prompt=chat_prompt)

    # Run the conversation chain with the user input
    response = conversation_chain.run(input=input_text)
    return response

