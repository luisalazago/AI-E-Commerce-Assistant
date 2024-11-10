# AI-E-Commerce-Assistant

This is a repository about an AI chatbot that assist to buy products from a catalogue.

## Introduction

This project use languages and components such as Python, HTML and CSS. The version of the components from the project are:

* Python 3.12.4
* Pip 24.0
* Flask 3.0.3
* OpenAI 1.54.3
* Dotenv 1.0.1

The main goal of this project is the user can interact with an assitant and this assistant helps the user to choose something from a basic catalogue. The important subject is the interactions that the chatbot cand do with the user.

## Run the project

To run the project you have to execute the file

> interfaceConsole.py

This file will execute console interface in the shell of your device and you will interact with the options of the program. The file use other files in the folder **assistant**, there are: a example of a chat assistant and the file of the assistant.

The project is documented in each *Python* file to explain some complex things that are not easy to understand, also the next section will explain a bit about some functions and the logic of the files.

## Functions and Files of the project

I will divide this section in the folders of the projects and then in the files.

### SRC

In this folder you can find other folders as: assistant, static and templates. The file

> main.py

This file is a *Python* file that use Flask and other functions to run a web app.

> product_catalogue.json

This file has the information about the products with the attributes asked by the test.

> interfaceConsole.py

This file has the graphic interface that lets the user interact with the assistant, this file use two additional functions to interact with the assistant and to know the products that the store has (just the names).

### Assistant

In this folder you will find two *Python* files: an example about a chat assistant and the file with the chat assistant use in the interface.

> e_commerceAssistantAI.py

In this file you will find the logic and the implementation of the assistant. The assistant has a default message to understand the context of the chat and what kind of messages it will get from the costumer.

```py
messages = [{"role": "system", "content": "You are SassySales, you are a helpful customer assistant that assist the customer answering their questions using the supplied tools, at the end of each answer recommend with a short text the product asked or many products if the customer asked for many of them."}]
```

Also we execute the model to get a call id, with this call the model do a calling function (if prompt requires it).

```py
response = get_assistant_answer(messages, tools = tools, tool_choice = "auto")
```

Then, with the call id the model use the calling functions to get the information asked by the user, to know wich function is necessary to execute the model knows it, so it decides which one use and a new message with the infromation. Finaly the model execute one more time to get the final answer to the user.

```py
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
```

### Static and Templates

These folders has the HTML file

> index.html

And the CSS file

>index.css

These files are not use in the interface of the project, because the project rigth now only works in shell.

## Notes from the project

The project rigth now is in its first version, by the time I could not finish the interface using Flask and HTML, but the interface is done to use in the consolo. In the future the interface will be finished to use as a wep app, using Flask, HTML and CSS. This future version of the project will have cards to show the products and show the conversation between the assistant and the user.

## Author

Luis Alberto Salazar Gómez.

Email: <luisalazago@gmail.com>

LinkedIn profile: <https://www.linkedin.com/in/luisalazago/>
