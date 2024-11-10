"""
This project is made by Luis Alberto Salazar.
You can find the repository in: https://github.com/luisalazago/AI-E-Commerce-Assistant
"""

# Libraries used.
import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Api Key used to OpenAI.
openai.api_key = os.environ.get("api_key")

# Products of the store.
catalogue = open("product_catalogue.json", "r")
catalogue = json.load(catalogue)

# Functions to call from the model (The catalogue is JSON file).
def getProductInfo(product_name: str):
    return str(catalogue[product_name])

def getProductNames():
    names = "" # Add the names to a temporary string to return.
    for product in catalogue:
        names += catalogue[product]["name"]
    return names

def checkStock(product_name: str):
    return catalogue[product_name]["stock"]

def checkName(product_name: str):
    return product_name in catalogue

# Virtual assistant to interact with the customer.
def get_assistant_answer(messages, model = "gpt-4o", tools = None, tool_choice = None):
    assistant = openai.chat.completions.create(
        model = model,
        messages = messages,
        tools = tools,
        tool_choice = tool_choice
    )
    return assistant.choices[0].message

# Main function to run the interface.
def main(prompt_user):
    # Tools to pass to the assistant
    tools = [
            {
                "type": "function",
                "function": {
                    "name": "getProductInfo",
                    "description": "Get the product information for a customer's question. Call this whenever you need to know a product information such as price, description, name, stock and product id, for example when a customer asks 'What is the cheapest product?'",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "The product name gave from the customer."
                            },  
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
    ]

    # Messages from the user. The message default is for make the model understand that is a sales assistant.
    messages = [{"role": "system", "content": "You are SassySales, you are a helpful customer assistant that assist the customer answering their questions using the supplied tools, at the end of each answer recommend with a short text the product asked or many products if the customer asked for many of them."}]
    messages.append(
        {
            "role": "user",
            "content": prompt_user
        }
    )

    # Get the function called by first time to generate a tool call.
    response = get_assistant_answer(messages, tools = tools, tool_choice = "auto")
    response = json.loads(response.model_dump_json())

    # This conditional is for the user in case input a promnpt that not use a function call.
    if response["tool_calls"] != None:
        # Delete the function call to add the message to the list of messages and then, add the result of the function calling.
        response["content"] = str(response["tool_calls"][0]["function"])
        del response["function_call"]

    messages.append(response)

    if response["tool_calls"] != None:
        ans_func = None
        function_name = response["tool_calls"][0]["function"]["name"]
        
        # This conditional analyze which function is need to call.
        if function_name == "getProductNames": ans_func = getProductNames()
        else:
            params = json.loads(response["tool_calls"][0]["function"]["arguments"])
            name = params["product_name"]
            check = checkName(name) # Check if the name passed by the customer is correct in the catalogue.
            if check:
                if function_name == "getProductInfo": ans_func = getProductInfo(name)
                elif function_name == "checkStock": ans_func = checkStock(name)
            else: return "Invalid name, please enter the correct name."

        # Add a new message with the result of the function call to inform the assistant.
        messages.append(
            {
                "role": "tool",
                "tool_call_id": response["tool_calls"][0]["id"],
                "name": function_name,
                "content": ans_func
            }
        )

    # At the end we generate the final answer using the messages again to get the answer with the function called.
    response = get_assistant_answer(messages, tools = tools)
    return response.content
