import requests
import os
from langchain.agents import Tool, create_structured_chat_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import json

# from langchain_core.output_parsers import TextOutputParser

# Replace the default JSON parser with a plain text parser


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key, temperature=0.5)

swagger_url = "http://127.0.0.1:8000/swagger.json"
swagger_response = requests.get(swagger_url)

# Check if the response is successful
if swagger_response.status_code == 200:
    try:
        swagger_json = swagger_response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON. Response text:")
        print(swagger_response.text)
else:
    print(f"Failed to fetch Swagger JSON. Status code: {swagger_response.status_code}")
    print(swagger_response.text)


# Custom function to make API calls based on Swagger JSON
def api_call(action, data=None):
    url = "http://127.0.0.1:8000/api/order/"
    headers = {"Content-Type": "application/json"}

    if action == "create":
        response = requests.post(url, json=data, headers=headers)
    elif action == "retrieve":
        response = requests.get(f"{url}{data['id']}/", headers=headers)
    elif action == "update":
        response = requests.put(f"{url}{data['id']}/", json=data, headers=headers)
    elif action == "delete":
        response = requests.delete(f"{url}{data['id']}/", headers=headers)
    else:
        return "Invalid action"

    if response.status_code in (200, 201):
        return response.json()
    elif response.status_code == 204:
        return "Successfully deleted"
    else:
        return f"Error: {response.status_code} - {response.text}"


class APITool:
    def _init_(self, action):
        self.action = action

    def _call_(self, tool_input):
        if isinstance(tool_input, str):
            try:
                data = json.loads(tool_input)
            except json.JSONDecodeError:
                data = {"id": tool_input}
        else:
            data = tool_input

        return api_call(self.action, data)


# Define CRUD tools
create_tool = Tool(
    name="CreateProduct",
    func=APITool("create"),
    description='Creates a new product. Provide "name", "description", and "price" fields only.'
)

retrieve_tool = Tool(
    name="RetrieveProduct",
    func=APITool("retrieve"),
    description='Retrieves a product by its "id".'
)

update_tool = Tool(
    name="UpdateProduct",
    func=APITool("update"),
    description='Updates a product by its "id". Provide updated "name", "description", or "price" only.'
)

delete_tool = Tool(
    name="DeleteProduct",
    func=APITool("delete"),
    description='Deletes a product by its "id".'
)

fake_chat_history = [
    {"sender": "user", "message": "Hi, I need help with my phone."},
    {"sender": "agent", "message": "Sure, what seems to be the problem?"},
    {"sender": "user", "message": "The battery drains too quickly."},
    {"sender": "agent", "message": "I see. How long does the battery last after a full charge?"},
    {"sender": "user", "message": "Only a few hours."},
    {"sender": "agent", "message": "That sounds like a battery issue. Have you tried any troubleshooting steps?"},
    {"sender": "user", "message": "Yes, I have tried restarting the phone and reducing screen brightness."},
    {"sender": "agent",
     "message": "Those are good steps. You might need to replace the battery if the issue persists."},
    {"sender": "user", "message": "Okay, thank you for the advice."},
    {"sender": "agent", "message": "You're welcome! Let me know if you need any further assistance."}
]


def analyze_sentiment(text, fkh=fake_chat_history):
    prompt = f"""
    You are an intelligent customer care agent. Perform sentiment analysis for every statement that is not a CRUD request and respond with only the score between -1 and 1 based on the user's interest.
    Text: {text}
    History: {fkh}
    """
    return llm.invoke(prompt)


sentiment_tool = Tool(
    name="SentimentAnalysis",
    func=analyze_sentiment,
    description="Analyze the sentiment of the input text."
)

# # Define structured agent configuration
# agent_config = {
#     "tools": [create_tool, retrieve_tool, update_tool, delete_tool, sentiment_tool],
#     "llm": llm,
#     "prompt": prompt_template,
#     "agent_type": "structured_chat",
#     "handle_parsing_errors": True
# }
# Define the prompt with 'agent_scratchpad' included
# Function to handle intermediate steps
response_schemas = [
    ResponseSchema(name="response", description="The agent's response to the user query"),
    ResponseSchema(name="sentiment_score", description="Sentiment score between -1 and 1")
]

# Create the output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)


def format_log_to_str(steps):
    # Safely handle missing 'intermediate_steps' by defaulting to an empty list
    steps = steps.get("intermediate_steps", [])
    return "\n".join([str(step) for step in steps])


# Define the prompt template, including 'agent_scratchpad'
prompt_template = PromptTemplate(
    input_variables=["input", "chat_history", "tools", "tool_names", "agent_scratchpad"],
    template="""
    You are an intelligent customer care agent. Your purpose is to respond smartly to user queries, analyze sentiment for every statement that is not a CRUD request, and respond with a score between -1 and 1 based on the user's interest.

    User Input: {input}
    Chat History: {chat_history}
    Tools: {tools}
    Tool Names: {tool_names}
    Agent Scratchpad: {agent_scratchpad}

    {format_instructions}
    """,
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)


class CustomJSONOutputParser:
    def parse(self, text):
        # Try to extract JSON using regex
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # If JSON parsing fails, create a structured response
        return {
            "response": text,
            "sentiment_score": 0  # default score
        }


# Initialize the structured agent
structured_agent = create_structured_chat_agent(
    tools=[create_tool, retrieve_tool, update_tool, delete_tool, sentiment_tool],
    llm=llm,
    prompt=prompt_template
)


def process_agent_response(response_text):
    try:
        # Try to parse the entire response as JSON
        parsed_response = json.loads(response_text)
        return parsed_response
    except json.JSONDecodeError:
        # If that fails, use the custom parser
        parser = CustomJSONOutputParser()
        return parser.parse(response_text)


# structured_agent.output_parser = TextOutputParser()

# Example query to invoke the agent
def handle_user_query(query, history):
    try:
        # Invoke the agent
        response = structured_agent.invoke({
            "input": query,
            "chat_history": history,
            "tools": [],
            "tool_names": [],
            "agent_scratchpad": [],
            "intermediate_steps": []
        })

        # Process the response
        parsed_response = process_agent_response(response['output'])

        # Print formatted output
        print("\nResponse:", parsed_response['response'])
        print("Sentiment Score:", parsed_response['sentiment_score'])

        return parsed_response

    except Exception as e:
        # If there's an error, try to extract useful information from the error message
        error_text = str(e)
        if "Could not parse LLM output:" in error_text:
            # Extract the JSON string from the error message
            json_start = error_text.find('{')
            json_end = error_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                try:
                    json_str = error_text[json_start:json_end]
                    parsed_response = json.loads(json_str)

                    # Print formatted output
                    print("\nResponse:", parsed_response['response'])
                    print("Sentiment Score:", parsed_response['sentiment_score'])

                    return parsed_response
                except json.JSONDecodeError:
                    pass

        print(f"Error processing query: {e}")
        return None


# Example usage
