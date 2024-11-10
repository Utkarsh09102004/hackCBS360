import requests
import os
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv

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
    url = "http://127.0.0.1:8000/api/products/"
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

    if response.status_code == 200 or response.status_code == 201:
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
                import json
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
    name="orderId",
    func=APITool("retrieve"),
    description='Retrieves a product by its "orderId".'
)

update_tool = Tool(
    name="UpdateOrderStatus",
    func=APITool("update"),
    description='Updates a product by its "id" and provided status '
)

delete_tool = Tool(
    name="DeleteProduct",
    func=APITool("delete"),
    description='Deletes a product by its "id".'
)


def analyze_sentiment(text):
    prompt = f"""
    You are an intelligent customer care agent whose purpose is to perform sentiment anarespond with only the score between -1 and 1 based on user's interest
    Text: {text}
    """

    return llm.invoke(prompt)


sentiment_tool = Tool(
    name="SentimentAnalysis",
    func=analyze_sentiment,
    description="Analyze the sentiment of the input text."
)

agent = initialize_agent(
    tools=[create_tool, retrieve_tool, update_tool, delete_tool, sentiment_tool],
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=False,
    handle_parsing_errors=True,
)

user_message = "You are an intelligent customer care agent whose purpose is to respond smartly to the user queries and analyze the sentiment for every statement that is not a CRUD request of the following text and respond with only the score between"
query = user_message + "My phone is facing issues with the battery. Can you help me with that?"
response = agent.invoke(query)
print(response)