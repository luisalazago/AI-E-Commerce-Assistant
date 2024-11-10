"""
This project is made by Luis Alberto Salazar.
You can find the repository in: https://github.com/luisalazago/AI-E-Commerce-Assistant
"""

# Libraries used.
import json
import os
import time
import assistant.e_commerceAssistantAI
from os import system

assistant = assistant.e_commerceAssistantAI

# Functions to run the project.
def showProducts():
    # This function only shows the name of the products to ask correctly to the assistant
    catalogue = open("product_catalogue.json", "r")
    catalogue = json.load(catalogue)
    
    system("cls")
    for product in catalogue: print("Product name: {}".format(product))
    print("")
    
    x = input("Do you want to go back to the menu? (y/n): ").lower()
    if x == 'y':
        system("cls")
        main()
    else:
        print("")
        print("Goodbye and have a good day. Until the next time!")
        exit(0)

def chatAndTalk():
    # This function simulates the interaction with the assistant.
    system("cls")
    print("Please, remember use the exactly names shown of the products to asked the assistant.")
    print("When you want to go back or exit to the chat use the word 'bye'") 
    print("===========================================================================================")
    print("")
    
    user = "user"
    user = str(input("Introduce your name: "))
    print("")
    
    print("SassySales/> {}".format(assistant.main("Hi, my name is " + user + " who are you?")))
    prompt = str(input(user + "/> "))
    
    flag_chat = True
    while flag_chat:
        print("SassySales/> {}".format(assistant.main(prompt)))
        if "bye" in prompt.lower(): flag_chat = False
        else: prompt = str(input(user + "/> "))
    
    time.sleep(5)
    system("cls")

# Main function.
def main():
    flag = True
    while flag: # When the flag is false the program turns off.
        print("===========================================================================================")
        print("")
        print("Welcome to SassySales, your bot assistant to help you with the products of the store!")
        print("")
        print("===========================================================================================")
        print("")
        print("What do you want to do?")
        print("[1] Show the products.")
        print("[2] Ask and chat about the products.")
        print("[3] Exit :c")
        print("")
        
        x = int(input("Choose the number of the options: "))
        
        while x > 3 or x < 1:
            x = input("Please, choose a correct option: ")
        
        if x == 1: showProducts()
        elif x == 2: chatAndTalk()
        else:
            flag = False
            print("")
            print("Goodbye and have a good day. Until the next time!")
            exit(0)
main()           