from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

import os
import json
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("api_key")
client = OpenAI(api_key = OPENAI_API_KEY)

catalogue = open("product_catalogue.json")
catalogue = json.load(catalogue)

def getProductInfo(product_name: str):
    return catalogue[product_name]

def getProductNames():
    temp = []
    for product in catalogue:
        temp.append(product["name"])
    return temp

def checkStock(product_name: str):
    return catalogue[product_name]["stock"]

assistant = client.beta.assistants.create(
    name="SassySales",
    instructions="You are a personal store assistant that helps users with their questions about products of the store, the store sells cellphones. Analyze the information about the products and give the user an answer using this information. Also at the end of an answer give them a short recomendation about the product or products asked.",
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
        }
    ],
    model="gpt-4o",
)