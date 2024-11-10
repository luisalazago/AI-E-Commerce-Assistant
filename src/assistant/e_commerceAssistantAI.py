# Libraries used.
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

import os
import json
from dotenv import load_dotenv
load_dotenv()

# Api Key used to OpenAI.
OPENAI_API_KEY = os.environ.get("api_key")
client = OpenAI(api_key = OPENAI_API_KEY)

# Products of the store.
catalogue = open("product_catalogue.json", "r")
catalogue = json.load(catalogue)

# Functions to call from the model.
def getProductInfo(product_name: str):
    return catalogue[product_name]

def getProductNames():
    names = []
    for product in catalogue:
        names.append(product["name"])
    return names

def checkStock(product_name: str):
    return catalogue[product_name]["stock"]

# Virtual assistant to interact with the customer.
assistant = client.beta.assistants.create(
    name="SassySales",
    instructions="You are a personal store assistant that helps users with their questions about products of the store, the store sells cellphones. Analyze the information about the products and give the customer an answer using this information. Also at the end of an answer give them a short recomendation about the product or products asked.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "getProductInfo",
                "description": "Get the product information for a customer's question. Call this whenever you need to know a product information, for example when a customer asks 'What is the cheapest product?'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The product name gave from the customer."
                        }   
                    },
                    "required": ["product_name"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "checkStock",
                "description": "Get the stock value of a product for a customer's question. Call this whenever you need to know the stock of a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The product name gave from the customer."
                        }   
                    },
                    "required": ["product_name"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "getProductNames",
                "description": "Get the name of the products for a customer's question. Call this whenever you need to know the names of the products from the store, for example when a customer asks 'Which products the store sells?'",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            }
        }
    ],
    model="gpt-4o",
)

thread = client.beta.threads.create()

response_message = ""
run = None

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Which products do you sell?"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Customer. The user has a premium account."
)

print(run)
        
while response_message == "":
    print("Iteration")
    if run.status == "requires_action":
        run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=run.thread_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
                    "output": response_message
                }
            ]
        )
            
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response_message = messages.data[0].content[0].text
        print(response_message)
