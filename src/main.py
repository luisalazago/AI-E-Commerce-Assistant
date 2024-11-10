"""
This project is made by Luis Alberto Salazar.
You can find the repository in: https://github.com/luisalazago/AI-E-Commerce-Assistant
"""

from flask import Flask, render_template, url_for
import assistant.e_commerceAssistantAI

app = Flask(__name__)
assistant = assistant.e_commerceAssistantAI

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
